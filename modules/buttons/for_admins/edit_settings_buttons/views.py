from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator

import discord

from modules.buttons.other_buttons.back import BackButton

from modules.buttons.for_admins.edit_settings_buttons.buttons.hidden_channels import (
    AddHiddenChannelButton,
    DeleteHiddenChannelButton
)
from modules.buttons.for_admins.edit_settings_buttons.buttons.hidden_roles import (
    AddHiddenRoleButton,
    DeleteHiddenRoleButton
)
from modules.buttons.for_admins.edit_settings_buttons.buttons.sys_channels import (
    AddSystemChannelsButton,
    DeleteSystemChannelsButton
)


class HiddenChannelsMenuView(discord.ui.View):
    def __init__(self, navigator: Navigator):
        super().__init__(timeout=60)

        self.add_item(AddHiddenChannelButton(navigator=navigator))
        self.add_item(DeleteHiddenChannelButton(navigator=navigator))
        self.add_item(BackButton(navigator=navigator))


class HiddenRolesMenuView(discord.ui.View):
    def __init__(self, navigator: Navigator):
        super().__init__(timeout=60)

        self.add_item(AddHiddenRoleButton(navigator=navigator))
        self.add_item(DeleteHiddenRoleButton(navigator=navigator))
        self.add_item(BackButton(navigator=navigator))


class SystemChannelsMenuView(discord.ui.View):
    def __init__(self, navigator: Navigator):
        super().__init__(timeout=60)

        self.add_item(AddSystemChannelsButton(navigator=navigator))
        self.add_item(DeleteSystemChannelsButton(navigator=navigator))
        self.add_item(BackButton(navigator=navigator))
