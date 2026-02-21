from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from ui.button_protection.admin_buttons_protection import FirewallButton

from features.for_admins.edit_settings.flows.main_settings import MainSettingsFlow

if TYPE_CHECKING:
    from core.navigator import Navigator
    from features.for_admins.edit_settings.services.main_settings import MainSettingsService
    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter


class MainSettingsButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            main_settings_service: MainSettingsService,
            formatter: SettingsFormatter
    ):
        super().__init__(
            label='Edit main settings',
            style=discord.ButtonStyle.green
        )
        self.main_settings_service = main_settings_service
        self.navigator = navigator
        self.formatter = formatter

    async def on_click(self, interaction: discord.Interaction) -> None:
        flow = MainSettingsFlow(
            main_settings_service=self.main_settings_service,
            formatter=self.formatter,
            navigator=self.navigator
        )

        await flow.start_for_main(interaction=interaction)
