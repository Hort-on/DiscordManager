from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.routes import Route
from features.for_admins.edit_settings.flows.main_settings.verification_role_flow import VerificationRoleFlow

from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from features.for_admins.edit_settings.services.main_settings.main_service import MainSettingsService
    from features.for_admins.edit_settings.services.main_settings.role_service import VerificationRoleService
    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter


class MainSettingsFlow:
    def __init__(
            self,
            navigator: Navigator,
            context: NavigationContext,
            main_settings_service: MainSettingsService,
            service_for_role: VerificationRoleService,
            formatter: SettingsFormatter,
    ):

        self.navigator = navigator
        self.context = context
        self.service = main_settings_service
        self.service_for_role = service_for_role
        self.formatter = formatter

    async def start_for_main(self, interaction: discord.Interaction):
        options = self._build_settings_options(guild_id=interaction.guild_id)

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the setting you want to change.',
            callback=self._proceed_value
        )

        view.context = self.context
        self.context.push(target=Route.SETTINGS_MENU)

        embed = self.formatter.format_current_main_settings(interaction)

        await interaction.response.edit_message(
            view=view,
            embed=embed
        )

    async def _proceed_value(self, interaction: discord.Interaction, value: list[str]) -> None:
        match value[0]:
            case 'verification_role_id':
                role_flow = VerificationRoleFlow(
                    navigator=self.navigator,
                    context=self.context,
                    formatter=self.formatter,
                    verification_role_service=self.service_for_role
                )

                await role_flow.show_available_roles(interaction=interaction)
                return

            case 'language':
                result = await self.service.save_new_language(guild_id=interaction.guild_id)
                if not result:
                    error_embed = ErrorEmbed(
                        description='Something went wrong, please try again later.'
                    )
                    await interaction.response.edit_message(embed=error_embed)
                    return

                settings_embed = self.formatter.format_current_main_settings(interaction)
                success_embed = SuccessEmbed(
                    description='Language is successfully changed'
                )

                await interaction.response.edit_message(
                    embeds=[settings_embed, success_embed]
                )

            case _:
                result = await self.service.save_new_value(
                    guild=interaction.guild,
                    config_key=value[0]
                )

                if not result:
                    error_embed = ErrorEmbed(
                        description='Something went wrong, please try again later.'
                    )
                    await interaction.response.edit_message(embed=error_embed)
                    return

                current_value = self.service.is_setting_enabled(
                    guild_id=interaction.guild_id,
                    config_key=value[0]
                )
                formatted = value[0].replace('_', ' ').title()

                success_embed = SuccessEmbed(
                    description=f"{formatted} is successfully {'enabled' if current_value else 'disabled'}"
                )

                settings_embed = self.formatter.format_current_main_settings(interaction)

                await interaction.response.edit_message(
                    embeds=[settings_embed, success_embed]
                )

    def _build_settings_options(self, guild_id: int) -> list[discord.SelectOption]:
        current_settings = self.service.get_main_settings(
            guild_id=guild_id
        )

        keys_to_skip = ['guild_id', 'verification_message_id']

        return [
            discord.SelectOption(
                label=k.replace('_', ' ').title(),
                value=k
            )
            for k, v in sorted(current_settings.items(), key=lambda item: item[0]) if k not in keys_to_skip
        ]
