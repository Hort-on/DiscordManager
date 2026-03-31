from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.params_containers import AdminMenuParams
from core.navigator.routes import Route

from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from features.for_admins.edit_settings.services.main_settings.role_service import VerificationRoleService
    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter
    from general_services.translator.translator import Translator


class VerificationRoleFlow:
    def __init__(
            self,
            navigator: Navigator,
            context: NavigationContext,
            formatter: SettingsFormatter,
            verification_role_service: VerificationRoleService,
            translator: Translator
    ):

        self.context = context
        self.navigator = navigator
        self.formatter = formatter
        self.service = verification_role_service
        self.translator = translator

    async def show_available_roles(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        assert guild is not None

        options = self._get_available_roles(guild=guild)

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            translator=self.translator,
            guild_id=guild.id,
            placeholder=self.translator.t(
                guild_id=guild.id,
                section='EDIT_SETTINGS',
                key='ask_ver_role'
            ),
            callback=self._save_verification_role
        )

        view.context = self.context

        self.context.push(
            target=Route.ADMIN_MENU,
            params=AdminMenuParams(guild_id=guild.id)
        )

        await interaction.response.edit_message(view=view)

    def _get_available_roles(self, guild: discord.Guild) -> list[discord.SelectOption]:
        hidden_roles = self.service.get_hidden_roles(guild_id=guild.id)

        return [
            discord.SelectOption(
                label=role.name,
                value=str(role.id)
            )
            for role in guild.roles if role.id not in hidden_roles
        ]

    async def _save_verification_role(self, interaction: discord.Interaction, value: list[str]) -> None:
        guild = interaction.guild
        assert guild is not None

        result = await self.service.save_role(guild_id=guild.id, role_id=int(value[0]))

        if not result:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=guild.id,
                    section='SYSTEM_GENERAL',
                    key='error_msg'
                )
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        role = guild.get_role(int(value[0]))
        if not role:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=guild.id,
                    section='SYSTEM_GENERAL',
                    key='error_msg'
                )
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        success_embed = SuccessEmbed(
            description=self.translator.t(
                guild_id=guild.id,
                section='EDIT_SETTINGS',
                key='ver_role_success',
                role_name=role.name
            )
        )

        settings_embed = self.formatter.format_current_main_settings(interaction)

        await interaction.response.edit_message(
            embeds=[settings_embed, success_embed]
        )
