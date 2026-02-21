from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator_context import NavigationContext

from features.for_admins.superusers.modals import AddSuperusersModal

from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed, WarningEmbed, InfoEmbed

if TYPE_CHECKING:
    from core.navigator import Navigator
    from features.for_admins.superusers.services import SuperusersService
    from features.for_admins.superusers.formatter import SuperusersFormatter


class SuperusersFlow:
    def __init__(
            self,
            navigator: Navigator,
            superusers_service: SuperusersService,
            formatter: SuperusersFormatter
    ):
        self.navigator = navigator
        self.superusers_service = superusers_service
        self.formatter = formatter

    # ================================= METHODS FOR ADD BUTTON =================================
    async def start_for_add(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(AddSuperusersModal(
            flow=self
        ))

    async def save_members(self, interaction: discord.Interaction, user_names: str) -> None:
        result = await self.superusers_service.prepare_users_for_addition(
            guild=interaction.guild,
            user_names=user_names
        )

        error_embed = result.get('error_embed', None)
        if error_embed:
            embed = ErrorEmbed(
                description=error_embed
            )
            await interaction.response.edit_message(
                embed=embed
            )
            return

        embeds: list[discord.Embed] = []

        success = result.get('success_embed', None)
        if success:
            success_embed = SuccessEmbed(
                description=success
            )
            embeds.append(success_embed)

        warning_e = result.get('warning_embed', None)
        if warning_e:
            warning_embed = WarningEmbed(
                description=warning_e
            )
            embeds.append(warning_embed)

        info = result.get('info_embed', None)
        if info:
            info_embed = InfoEmbed(
                description=info
            )
            embeds.append(info_embed)

        await interaction.response.edit_message(
            embeds=embeds
        )

    # ================================= METHODS FOR DELETE BUTTON =================================
    async def start_for_delete(self, interaction: discord.Interaction):
        options, not_found = await self._build_options(
            guild=interaction.guild,
            client=interaction.client
        )

        if not options:
            embed = ErrorEmbed(
                description='No superusers were found.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the users you want to delete:',
            callback=lambda i, v: self._send_result(i, v, not_found),
            max_values=min(25, len(options))
        )

        context = getattr(view, 'context', NavigationContext())

        context.push(target='superusers_menu')

        view.context = context

        info_embed = self.formatter.build_embed(guild=interaction.guild)

        await interaction.response.edit_message(
            embed=info_embed,
            view=view
        )

    async def _send_result(
            self,
            interaction: discord.Interaction,
            values: list[str],
            not_found: str
    ):
        result = await self.superusers_service.delete_superusers(
            guild_id=interaction.guild_id,
            values=values
        )
        if not result:
            warning_embed = WarningEmbed(
                description='Something went wrong, please try again later.'
            )

            await interaction.response.edit_message(
                embed=warning_embed
            )
            return

        embeds: list[discord.Embed] = []
        deleted_usernames: list[str] = ['These users were not on this server and were deleted as well:',
                                        f'{'-' * 40}']

        for user_id in values:
            user = await interaction.guild.fetch_member(int(user_id))
            deleted_usernames.append(f'🔸{user.display_name}')

        success_embed = SuccessEmbed(
            description='\n'.join(deleted_usernames)
        )
        embeds.append(success_embed)

        if not_found:
            warning_embed = WarningEmbed(
                description=not_found
            )
            embeds.append(warning_embed)

        current_superusers = self.formatter.build_embed(
            guild=interaction.guild
        )
        embeds.append(current_superusers)

        await interaction.response.edit_message(
            embeds=embeds
        )

    async def _build_options(self, guild: discord.Guild, client: discord.Client) -> tuple:
        users, not_found = await self.superusers_service.get_superusers_for_deletion(
            guild=guild,
            client=client
        )

        options = [
            discord.SelectOption(
                label=value,
                value=str(key)
            )
            for key, value in users.items()
        ]

        return options, not_found
