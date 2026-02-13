from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.navigator import Navigator

import discord

from modules.buttons.other_buttons.back import BackButton
from modules.buttons.for_admins.edit_settings_buttons.buttons.hidden_channels import HiddenChannelsMenuButtons
from modules.buttons.for_admins.edit_settings_buttons.buttons.hidden_roles import HiddenRolesMenuButton
from modules.buttons.for_admins.edit_settings_buttons.buttons.main_settings import MainSettingsButton
from modules.buttons.for_admins.edit_settings_buttons.buttons.sys_channels import SystemChannelsMenuButton


class SettingsMenuView(discord.ui.View):
    def __init__(self, navigator: Navigator):
        super().__init__(timeout=60)

        self.add_item(MainSettingsButton(navigator=navigator))
        self.add_item(SystemChannelsMenuButton(navigator=navigator))
        self.add_item(HiddenChannelsMenuButtons(navigator=navigator))
        self.add_item(HiddenRolesMenuButton(navigator=navigator))
        self.add_item(BackButton(navigator=navigator))
