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
    from features.for_admins.edit_settings.services.hidden_channels import HiddenChannelsService
    from features.for_admins.edit_settings.services.hidden_roles import HiddenRolesService
    from features.for_admins.edit_settings.services.system_channels import SystemChannelsService
    from general_services.other_services.cleanup_service import CleanUpService
    from ui.button_protection.button_protection_service import ButtonProtectionService


class SettingsMenuView(discord.ui.View):
    def __init__(
            self,
            navigator: Navigator,
            main_settings_service: MainSettingsService,
            settings_formatter: SettingsFormatter,
            buttons_protection: ButtonProtectionService,
            hidden_ch_service: HiddenChannelsService,
            hidden_role_service: HiddenRolesService,
            sys_channels_service: SystemChannelsService,
            cleanup_service: CleanUpService
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
            buttons_protection=buttons_protection,
            formatter=settings_formatter,
            service=sys_channels_service
        ))

        self.add_item(HiddenChannelsMenuButtons(
            navigator=navigator,
            buttons_protection=buttons_protection,
            formatter=settings_formatter,
            hidden_ch_service=hidden_ch_service,
            cleanup_service=cleanup_service
        ))

        self.add_item(HiddenRolesMenuButton(
            navigator=navigator,
            buttons_protection=buttons_protection,
            formatter=settings_formatter,
            hidden_roles_service=hidden_role_service,
            cleanup_service=cleanup_service
        ))

        self.add_item(BackButton(navigator=navigator))
