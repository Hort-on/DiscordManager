from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.routes import Route
from database.settings_storage.settings_manager import StorageTarget

from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed
from ui.drop_down_menu.drop_down_selector import DropMenuView

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext

    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter
    from features.for_admins.edit_settings.services.hidden_roles import HiddenRolesService

    from general_services.other_services.cleanup_service import CleanUpService
    from general_services.translator.translator import Translator


class HiddenRolesFlow:
    def __init__(
            self,
            navigator: Navigator,
            context: NavigationContext,
            formatter: SettingsFormatter,
            hidden_roles_service: HiddenRolesService,
            cleanup_service: CleanUpService,
            translator: Translator
    ):

        self.navigator = navigator
        self.context = context
        self.formatter = formatter
        self.hidden_roles_service = hidden_roles_service
        self.cleanup = cleanup_service
        self.translator = translator

    # ================================= METHODS FOR ADD BUTTON =================================
    async def start_for_add(self, interaction: discord.Interaction) -> None:
        options = self._get_available_roles(
            interaction=interaction
        )

        if not options:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=interaction.guild_id,
                    section='EDIT_SETTINGS',
                    key='no_roles_to_add'
                )
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            translator=self.translator,
            guild_id=interaction.guild_id,
            placeholder=self.translator.t(
                guild_id=interaction.guild_id,
                section='EDIT_SETTINGS',
                key='ask_role_placeholder'
            ),
            callback=self._save_role_to_hidden,
            max_values=min(25, len(options))
        )

        view.context = self.context

        self.context.push(target=Route.HIDDEN_ROLES_MENU)

        await interaction.response.edit_message(view=view)

    async def _save_role_to_hidden(self, interaction: discord.Interaction, values: list[str]) -> None:
        result = await self.hidden_roles_service.save_roles(
            guild_id=interaction.guild_id,
            values=values
        )

        if not result:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=interaction.guild_id,
                    section='SYSTEM_GENERAL',
                    key='error_msg'
                )
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        success_msg = self.translator.t(
            guild_id=interaction.guild_id,
            section='EDIT_SETTINGS',
            key='success_role_addition'
        )

        await self._send_result(
            interaction=interaction,
            values=values,
            first_line=success_msg
        )

    # ================================= METHODS FOR DELETE BUTTON =================================
    async def start_for_delete(self, interaction: discord.Interaction) -> None:
        embed = await self.formatter.format_current_hidden(
            interaction=interaction,
            target=StorageTarget.HIDDEN_ROLES
        )

        options = self._get_deletable_roles(
            interaction=interaction,
        )

        if not options:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=interaction.guild_id,
                    section='EDIT_SETTINGS',
                    key='no_roles_to_delete'
                )
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            translator=self.translator,
            guild_id=interaction.guild_id,
            placeholder=self.translator.t(
                guild_id=interaction.guild_id,
                section='EDIT_SETTINGS',
                key='ask_role_to_delete'
            ),
            callback=self._delete_role_procedure,
            max_values=min(25, len(options))
        )

        view.context = self.context

        self.context.push(target=Route.HIDDEN_ROLES_MENU)

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
                description=self.translator.t(
                    guild_id=interaction.guild_id,
                    section='SYSTEM_GENERAL',
                    key='error_msg'
                )
            )
            await interaction.response.edit_message(embed=error_embed)

        success_msg = self.translator.t(
                guild_id=interaction.guild_id,
                section='EDIT_SETTINGS',
                key='success_role_deletion'
            )

        await self._send_result(
            interaction=interaction,
            values=values,
            first_line=success_msg
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

        settings_embed = await self.formatter.format_current_hidden(
            interaction=interaction,
            target=StorageTarget.HIDDEN_ROLES
        )

        await interaction.response.edit_message(
            embeds=[settings_embed, success_embed]
        )

    async def for_roles_list(self, interaction: discord.Interaction):
        embed = await self.formatter.format_current_hidden(
            interaction=interaction,
            target=StorageTarget.HIDDEN_ROLES
        )
        await interaction.response.edit_message(embed=embed)
