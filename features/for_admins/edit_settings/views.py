from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.for_admins.edit_settings.buttons.hidden_channels import (
    AddHiddenChannelButton,
    DeleteHiddenChannelButton,
    HiddenChannelsListButton
)
from features.for_admins.edit_settings.buttons.hidden_roles import (
    AddHiddenRoleButton,
    DeleteHiddenRoleButton,
    HiddenRolesListButton
)
from features.for_admins.edit_settings.buttons.sys_channels import (
    AddSystemChannelsButton,
    DeleteSystemChannelsButton,
    SystemChannelsListButton
)

from ui.buttons.back_button import BackButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_admins.edit_settings.flows.sys_channels import SystemChannelsFlow
    from features.for_admins.edit_settings.flows.hidden_channels import HiddenChannelsFlow
    from features.for_admins.edit_settings.flows.hidden_roles import HiddenRolesFlow
    from ui.button_protection.button_protection_service import ButtonProtectionService


class HiddenChannelsMenuView(discord.ui.View):
    def __init__(
            self,
            navigator: Navigator,
            buttons_protection: ButtonProtectionService,
            flow: HiddenChannelsFlow
    ):
        super().__init__(timeout=60)

        self.add_item(AddHiddenChannelButton(
            buttons_protection=buttons_protection,
            flow=flow
        ))
        self.add_item(DeleteHiddenChannelButton(
            buttons_protection=buttons_protection,
            flow=flow
        ))
        self.add_item(HiddenChannelsListButton(
            buttons_protection=buttons_protection,
            flow=flow
        ))
        self.add_item(BackButton(navigator=navigator))


class HiddenRolesMenuView(discord.ui.View):
    def __init__(
            self,
            navigator: Navigator,
            buttons_protection: ButtonProtectionService,
            flow: HiddenRolesFlow
    ):
        super().__init__(timeout=60)

        self.add_item(AddHiddenRoleButton(
            buttons_protection=buttons_protection,
            flow=flow
        ))

        self.add_item(DeleteHiddenRoleButton(
            buttons_protection=buttons_protection,
            flow=flow
        ))

        self.add_item(HiddenRolesListButton(
            buttons_protection=buttons_protection,
            flow=flow
        ))

        self.add_item(BackButton(navigator=navigator))


class SystemChannelsMenuView(discord.ui.View):
    def __init__(
            self,
            navigator: Navigator,
            buttons_protection: ButtonProtectionService,
            flow: SystemChannelsFlow
    ):
        super().__init__(timeout=60)

        self.add_item(AddSystemChannelsButton(
            buttons_protection=buttons_protection,
            flow=flow
        ))

        self.add_item(DeleteSystemChannelsButton(
            buttons_protection=buttons_protection,
            flow=flow
        ))

        self.add_item(SystemChannelsListButton(
            buttons_protection=buttons_protection,
            flow=flow
        ))

        self.add_item(BackButton(navigator=navigator))
