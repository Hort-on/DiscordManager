from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from .results import DeleteSuperusersResult, AddSuperusersResult

from core.navigator.routes import Route
from features.for_admins.superusers.modal import AddSuperusersModal
from general_services.other_services.get_member_by_name import get_member_by_name

from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.embed_constructor.embed_constructor import ErrorEmbed

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from features.for_admins.superusers.services import SuperusersService
    from features.for_admins.superusers.formatter import SuperusersFormatter
    from general_services.translator.translator import Translator


class SuperusersFlow:
    def __init__(
        self,
        navigator: Navigator,
        context: NavigationContext,
        superusers_service: SuperusersService,
        formatter: SuperusersFormatter,
        translator: Translator
    ):
        self.navigator = navigator
        self.context = context
        self.superusers_service = superusers_service
        self.formatter = formatter
        self.translator = translator

    async def start_for_add(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(
            AddSuperusersModal(
                flow=self,
                translator=self.translator,
                guild_id=interaction.guild_id
            )
        )

    async def save_members(self, interaction: discord.Interaction, user_names: str) -> None:
        usernames = self._parse_usernames(user_names=user_names)
        current_superusers = self.superusers_service.get_current_superusers(guild_id=interaction.guild_id)

        result = self._proceed_users(
            guild=interaction.guild,
            usernames=usernames,
            current_superusers=current_superusers
        )

        if result.added_ids:
            success = await self.superusers_service.add_superusers(
                guild_id=interaction.guild_id,
                user_ids=set(result.added_ids)
            )
            if not success:
                await interaction.response.edit_message(
                    embed=ErrorEmbed(
                        description=self.translator.t(
                            guild_id=interaction.guild_id,
                            section='SYSTEM_GENERAL',
                            key='error_msg'
                        )
                    )
                )
                return

        embeds = self.formatter.build_add_result_embeds(
            result=result,
            guild_id=interaction.guild_id
        )

        await interaction.response.edit_message(embeds=embeds)

    @staticmethod
    def _parse_usernames(user_names: str) -> set[str]:
        return {name.strip() for name in user_names.split(',') if name.strip()}

    @staticmethod
    def _proceed_users(
            guild: discord.Guild,
            usernames: set[str],
            current_superusers: set[int]
    ) -> AddSuperusersResult:

        added_ids: set[int] = set()
        added_names: set[str] = set()
        not_found: set[str] = set()
        already_super: set[str] = set()

        for username in usernames:
            member = get_member_by_name(guild=guild, username=username)

            if not member:
                not_found.add(username)
                continue

            name = member.display_name or member.name

            if member.id in current_superusers:
                already_super.add(name)
                continue

            added_ids.add(member.id)
            added_names.add(name)

        return AddSuperusersResult(
            added_ids=added_ids,
            added_names=added_names,
            not_found=not_found,
            already_super=already_super
        )

    async def start_for_delete(self, interaction: discord.Interaction) -> None:
        users, not_found_msg = await self.superusers_service.get_superusers_for_deletion(
            guild=interaction.guild,
            client=interaction.client
        )

        if not users:
            await interaction.response.edit_message(
                embed=ErrorEmbed(
                    description=self.translator.t(
                        guild_id=interaction.guild_id,
                        section='SUPERUSERS',
                        key='no_superusers'
                    )
                )
            )
            return

        options = [
            discord.SelectOption(label=name, value=str(user_id))
            for user_id, name in users.items()
        ]

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            translator=self.translator,
            guild_id=interaction.guild_id,
            placeholder=self.translator.t(
                guild_id=interaction.guild_id,
                section='SUPERUSERS',
                key='ask_s_users_to_delete'
            ),
            callback=lambda i, v: self._handle_delete(i, v, not_found_msg),
            max_values=min(25, len(options))
        )

        view.context = self.context
        self.context.push(target=Route.SUPERUSERS_MENU)

        embed = self.formatter.build_embed(guild=interaction.guild)

        await interaction.response.edit_message(embed=embed, view=view)

    async def _handle_delete(
        self,
        interaction: discord.Interaction,
        values: list[str],
        not_found_msg: str | bool
    ) -> None:
        success = await self.superusers_service.delete_superusers(
            guild_id=interaction.guild_id,
            values=values
        )

        if not success:
            await interaction.response.edit_message(
                embed=ErrorEmbed(
                    description=self.translator.t(
                        guild_id=interaction.guild_id,
                        section='SYSTEM_GENERAL',
                        key='error_msg'
                    )
                )
            )
            return

        deleted_names: set[str] = set()

        for user_id in values:
            member = await interaction.guild.fetch_member(int(user_id))
            deleted_names.add(member.display_name)

        result = DeleteSuperusersResult(
            deleted=deleted_names,
            not_found_message=not_found_msg if not_found_msg else None
        )

        embeds = self.formatter.build_delete_result_embeds(
            result=result,
            guild=interaction.guild
        )

        await interaction.response.edit_message(embeds=embeds)

    async def for_superusers_list(self, interaction: discord.Interaction) -> None:
        embed = self.formatter.build_embed(guild=interaction.guild)
        await interaction.response.edit_message(embed=embed)
