from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.for_admins.edit_settings.flows.main_settings.main_flow import MainSettingsFlow

from ui.button_protection.admin_buttons_protection import FirewallButton


if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from features.for_admins.edit_settings.services.main_settings.main_service import MainSettingsService
    from features.for_admins.edit_settings.services.main_settings.role_service import VerificationRoleService
    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter
    from ui.button_protection.button_protection_service import ButtonProtectionService


class MainSettingsButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            context: NavigationContext,
            main_settings_service: MainSettingsService,
            service_for_role: VerificationRoleService,
            formatter: SettingsFormatter,
            buttons_protection: ButtonProtectionService
    ):
        super().__init__(
            label='Edit main settings',
            style=discord.ButtonStyle.green,
            protection_service=buttons_protection
        )

        self.navigator = navigator
        self.context = context
        self.main_settings_service = main_settings_service
        self.formatter = formatter
        self.service_for_role = service_for_role

    async def on_click(self, interaction: discord.Interaction) -> None:
        flow = MainSettingsFlow(
            main_settings_service=self.main_settings_service,
            formatter=self.formatter,
            navigator=self.navigator,
            context=self.context,
            service_for_role=self.service_for_role
        )

        await flow.start_for_main(interaction=interaction)
