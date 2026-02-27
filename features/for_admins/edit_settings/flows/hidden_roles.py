from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.navigator_context import NavigationContext
from core.navigator.routes import Route

from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed
from ui.drop_down_menu.drop_down_selector import DropMenuView

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator

    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter
    from features.for_admins.edit_settings.services.hidden_roles import HiddenRolesService

    from general_services.other_services.cleanup_service import CleanUpService


class HiddenRolesFlow:
    def __init__(
            self,
            navigator: Navigator,
            formatter: SettingsFormatter,
            hidden_roles_service: HiddenRolesService,
            cleanup_service: CleanUpService
    ):
        self.formatter = formatter
        self.navigator = navigator
        self.hidden_roles_service = hidden_roles_service
        self.cleanup = cleanup_service

    # ================================= METHODS FOR ADD BUTTON =================================
    async def start_for_add(self, interaction: discord.Interaction) -> None:
        options = self._get_available_roles(
            interaction=interaction
        )

        if not options:
            embed = ErrorEmbed(
                description='No available roles to be add.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the role you want to add to hidden:',
            callback=self._save_role_to_hidden,
            max_values=min(25, len(options))
        )

        context = getattr(view, 'context', None)
        if context is None:
            context = NavigationContext()
            view.context = context

        context.push(target=Route.HIDDEN_ROLES_MENU)

        await interaction.response.edit_message(view=view)

    async def _save_role_to_hidden(self, interaction: discord.Interaction, values: list[str]) -> None:
        result = await self.hidden_roles_service.save_roles(
            guild_id=interaction.guild_id,
            values=values
        )

        if not result:
            error_embed = ErrorEmbed(
                description='Something went wrong, please try again later.'
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        await self._send_result(
            interaction=interaction,
            values=values,
            first_line='These roles have been successfully added to hidden:'
        )

    # ================================= METHODS FOR DELETE BUTTON =================================
    async def start_for_delete(self, interaction: discord.Interaction) -> None:
        embed = await self.formatter.format_current_hidden_channels(interaction)

        options = self._get_deletable_roles(
            interaction=interaction,
        )

        if not options:
            embed = ErrorEmbed(
                description='No available channels to be deleted.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the role you want to delete:',
            callback=self._delete_role_procedure,
            max_values=min(25, len(options))
        )

        context = getattr(view, 'context', None)
        if context is None:
            context = NavigationContext()
            view.context = context

        context.push(target=Route.HIDDEN_ROLES_MENU)

        await interaction.response.edit_message(
            view=view,
            embed=embed
        )

    async def _delete_role_procedure(self, interaction: discord.Interaction, values: list[str]):
        result = self.hidden_roles_service.delete_roles(
            guild_id=interaction.guild_id,
            values=values,
        )

        if not result:
            error_embed = ErrorEmbed(
                description='Something went wrong, please try again later.'
            )
            await interaction.response.edit_message(embed=error_embed)

        await self._send_result(
            interaction=interaction,
            values=values,
            first_line='These roles have been successfully deleted from hidden:'
        )

    # ================================= METHODS FOR BOTH =================================
    def _get_available_roles(self, interaction: discord.Interaction) -> list[discord.SelectOption]:
        hidden_channels = self.hidden_roles_service.get_hidden_roles(
            guild_id=interaction.guild_id
        )

        return [
            discord.SelectOption(
                label=role.name,
                value=str(role.id)
            )
            for role in interaction.guild.roles if role.id not in hidden_channels
        ]

    def _get_deletable_roles(self, interaction: discord.Interaction) -> list[discord.SelectOption]:
        not_found_roles: set[int] = set()

        hidden_roles = self.hidden_roles_service.get_hidden_roles(
            guild_id=interaction.guild_id
        )

        available_roles: dict[int, str] = {}
        for role_id in hidden_roles:
            role = interaction.guild.get_role(role_id)

            if not role:
                not_found_roles.add(role_id)
                continue

            available_roles[role_id] = role.name

        if not_found_roles:
            self.cleanup.clean_up_hidden_roles(
                guild_id=interaction.guild_id,
                role_ids=not_found_roles
            )

        return [
            discord.SelectOption(
                label=value,
                value=str(key)
            )
            for key, value in sorted(available_roles.items(), key=lambda i: i[0])
        ]

    async def _send_result(
            self,
            interaction: discord.Interaction,
            values: list[str],
            first_line: str
    ):
        role_ids: set[int] = set(int(role_id) for role_id in values)

        role_names: list[str] = [first_line]
        for role_id in role_ids:
            role = interaction.guild.get_role(role_id)
            role_names.append(f'🔸 {role.name}')

        result_msg = '\n'.join(role_names)

        success_embed = SuccessEmbed(
            description=result_msg
        )

        settings_embed = await self.formatter.format_current_hidden_roles(interaction)

        await interaction.response.edit_message(
            embeds=[settings_embed, success_embed]
        )

    async def for_roles_list(self, interaction: discord.Interaction):
        embed = await self.formatter.format_current_hidden_roles(interaction)
        await interaction.response.edit_message(embed=embed)
