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


class SettingsMenuView(discord.ui.View):
    def __init__(
            self,
            navigator: Navigator,
            main_settings_service: MainSettingsService,
            settings_formatter: SettingsFormatter
    ):
        super().__init__(timeout=60)

        self.add_item(MainSettingsButton(
            navigator=navigator,
            main_settings_service=main_settings_service,
            formatter=settings_formatter
        ))
        self.add_item(SystemChannelsMenuButton(navigator=navigator))
        self.add_item(HiddenChannelsMenuButtons(navigator=navigator))
        self.add_item(HiddenRolesMenuButton(navigator=navigator))
        self.add_item(BackButton(navigator=navigator))
