from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.for_admins.edit_settings.buttons.hidden_channels import HiddenChannelsMenuButtons
from features.for_admins.edit_settings.buttons.hidden_roles import HiddenRolesMenuButton
from features.for_admins.edit_settings.buttons.main_settings import MainSettingsButton
from features.for_admins.edit_settings.buttons.sys_channels import SystemChannelsMenuButton

from ui.buttons.back_button import BackButton

if TYPE_CHECKING:
    from core.navigator import Navigator
    from features.for_admins.edit_settings.services.main_settings import MainSettingsService
    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter
    from ui.button_protection.button_protection_service import ButtonProtectionService


class SettingsMenuView(discord.ui.View):
    def __init__(
            self,
            navigator: Navigator,
            main_settings_service: MainSettingsService,
            settings_formatter: SettingsFormatter,
            buttons_protection: ButtonProtectionService
    ):
        super().__init__(timeout=60)

        self.add_item(MainSettingsButton(
            navigator=navigator,
            main_settings_service=main_settings_service,
            formatter=settings_formatter,
            buttons_protection=buttons_protection
        ))
        self.add_item(SystemChannelsMenuButton(
            navigator=navigator,
            buttons_protection=buttons_protection
        ))
        self.add_item(HiddenChannelsMenuButtons(
            navigator=navigator,
            buttons_protection=buttons_protection
        ))
        self.add_item(HiddenRolesMenuButton(
            navigator=navigator,
            buttons_protection=buttons_protection
        ))
        self.add_item(BackButton(navigator=navigator))
