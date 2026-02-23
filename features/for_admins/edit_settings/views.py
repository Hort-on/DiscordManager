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
    from core.navigator import Navigator
    from features.for_admins.edit_settings.services.hidden_channels import HiddenChannelsService
    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter
    from features.for_admins.edit_settings.services.hidden_roles import HiddenRolesService
    from features.for_admins.edit_settings.services.system_channels import SystemChannelsService
    from ui.button_protection.button_protection_service import ButtonProtectionService
    from general_services.other_services.cleanup_service import CleanUpService


class HiddenChannelsMenuView(discord.ui.View):
    def __init__(
            self,
            navigator: Navigator,
            hidden_ch_service: HiddenChannelsService,
            formatter: SettingsFormatter,
            cleanup_service: CleanUpService,
            buttons_protection: ButtonProtectionService
    ):
        super().__init__(timeout=60)

        self.add_item(AddHiddenChannelButton(
            navigator=navigator,
            hidden_ch_service=hidden_ch_service,
            formatter=formatter,
            cleanup_service=cleanup_service,
            buttons_protection=buttons_protection
        ))
        self.add_item(DeleteHiddenChannelButton(
            navigator=navigator,
            hidden_ch_service=hidden_ch_service,
            formatter=formatter,
            cleanup_service=cleanup_service,
            buttons_protection=buttons_protection
        ))
        self.add_item(HiddenChannelsListButton(
            formatter=formatter,
            buttons_protection=buttons_protection
        ))
        self.add_item(BackButton(navigator=navigator))


class HiddenRolesMenuView(discord.ui.View):
    def __init__(
            self,
            navigator: Navigator,
            formatter: SettingsFormatter,
            hidden_roles_service: HiddenRolesService,
            cleanup_service: CleanUpService,
            buttons_protection: ButtonProtectionService
    ):
        super().__init__(timeout=60)

        self.add_item(AddHiddenRoleButton(
            navigator=navigator,
            formatter=formatter,
            hidden_roles_service=hidden_roles_service,
            cleanup_service=cleanup_service,
            buttons_protection=buttons_protection
        ))
        self.add_item(DeleteHiddenRoleButton(
            navigator=navigator,
            formatter=formatter,
            hidden_roles_service=hidden_roles_service,
            cleanup_service=cleanup_service,
            buttons_protection=buttons_protection
        ))
        self.add_item(HiddenRolesListButton(
            formatter=formatter,
            buttons_protection=buttons_protection
        ))
        self.add_item(BackButton(navigator=navigator))


class SystemChannelsMenuView(discord.ui.View):
    def __init__(
            self,
            navigator: Navigator,
            sys_channels_service: SystemChannelsService,
            formatter: SettingsFormatter,
            buttons_protection: ButtonProtectionService
    ):
        super().__init__(timeout=60)

        self.add_item(AddSystemChannelsButton(
            navigator=navigator,
            sys_channels_service=sys_channels_service,
            formatter=formatter,
            buttons_protection=buttons_protection
        ))
        self.add_item(DeleteSystemChannelsButton(
            navigator=navigator,
            sys_channels_service=sys_channels_service,
            formatter=formatter,
            buttons_protection=buttons_protection
        ))
        self.add_item(SystemChannelsListButton(
            formatter=formatter,
            buttons_protection=buttons_protection
        ))
        self.add_item(BackButton(navigator=navigator))
