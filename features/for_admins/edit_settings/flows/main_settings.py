from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.navigator_context import NavigationContext
from core.navigator.params_containers import AdminMenuParams
from core.navigator.routes import Route

from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_admins.edit_settings.services.main_settings import MainSettingsService
    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter


class MainSettingsFlow:
    def __init__(
            self,
            main_settings_service: MainSettingsService,
            formatter: SettingsFormatter,
            navigator: Navigator,
    ):
        self.service = main_settings_service
        self.formatter = formatter
        self.navigator = navigator

    async def start_for_main(self, interaction: discord.Interaction):
        options = self._build_settings_options(guild_id=interaction.guild_id)

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the setting you want to change.',
            callback=self._proceed_value
        )

        context = getattr(view, 'context', None)
        if context is None:
            context = NavigationContext()
            view.context = context

        context.push(target=Route.SETTINGS_MENU)

        embed = self.formatter.format_current_main_settings(interaction)

        await interaction.response.edit_message(
            view=view,
            embed=embed
        )

    async def _proceed_value(self, interaction: discord.Interaction, value: list[str]) -> None:
        if value[0] == 'verification_role_id':
            options = [
                discord.SelectOption(
                    label=role.name,
                    value=str(role.id)
                )
                for role in interaction.guild.roles
            ]

            view = DropMenuView(
                navigator=self.navigator,
                options=options,
                placeholder='Please select the role:',
                callback=self._save_verification_role
            )

            context = getattr(view, 'context', None)
            if context is None:
                context = NavigationContext()
                view.context = context

            context.push(target=Route.ADMIN_MENU,
                         params=AdminMenuParams(
                             guild_id=interaction.guild_id
                         ))

            await interaction.response.edit_message(view=view)
            return

        result = await self.service.handle_setting_update(
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

        success_embed = SuccessEmbed(
            description=f"{value[0]} is successfully {'enabled' if current_value else 'disabled'}"
        )

        settings_embed = self.formatter.format_current_main_settings(interaction)

        await interaction.response.edit_message(
            embeds=[settings_embed, success_embed]
        )

    async def _save_verification_role(self, interaction: discord.Interaction, value: list[str]):
        result = await self.service.save_new_role(
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

    def _build_settings_options(self, guild_id: int) -> list[discord.SelectOption]:
        current_settings = self.service.get_main_settings(
            guild_id=guild_id
        )

        return [
            discord.SelectOption(
                label=k.replace('_', ' ').title(),
                value=k
            )
            for k, v in sorted(current_settings.items(), key=lambda item: item[0])
        ]
