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


class VerificationRoleFlow:
    def __init__(
            self,
            navigator: Navigator,
            context: NavigationContext,
            formatter: SettingsFormatter,
            verification_role_service: VerificationRoleService
    ):

        self.context = context
        self.navigator = navigator
        self.formatter = formatter
        self.service = verification_role_service

    async def show_available_roles(self, interaction: discord.Interaction) -> None:
        options = self._get_available_roles(guild=interaction.guild)

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the role:',
            callback=self._save_verification_role
        )

        view.context = self.context

        self.context.push(
            target=Route.ADMIN_MENU,
            params=AdminMenuParams(
                guild_id=interaction.guild_id
            )
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
        result = await self.service.save_role(
            guild_id=interaction.guild_id,
            role_id=int(value[0])
        )

        if not result:
            embed = ErrorEmbed(
                description='Somethings went wrong, please try again later'
            )
            await interaction.response.edit_message(embed=embed)
            return

        role = interaction.guild.get_role(int(value[0]))

        success_embed = SuccessEmbed(
            description=f'Verification role is successfully assigned to: {role.name}'
        )

        settings_embed = self.formatter.format_current_main_settings(interaction)

        await interaction.response.edit_message(
            embeds=[settings_embed, success_embed]
        )
