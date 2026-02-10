from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.buttons.for_admins.edit_settings_buttons.services.settings_formatter import SettingsFormatter
from modules.buttons.for_admins.edit_settings_buttons.services.main_settings import EditMainSettingsService

from services.buttons.navigator_context import NavigationContext
from services.drop_down_menu.drop_down_selector import DropMenuView


class MainSettingsButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Edit main settings',
            style=discord.ButtonStyle.green
        )
        self.service = EditMainSettingsService(navigator=navigator)
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='settings_menu')

        formatter = SettingsFormatter()
        embed = formatter.format_current_main_settings(interaction)

        options = self.service.build_options(guild_id=interaction.guild_id)

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the module you want to change.',
            callback=self.service.proceed_result
        )

        view.context = context

        await interaction.response.edit_message(
            view=view,
            embed=embed
        )
