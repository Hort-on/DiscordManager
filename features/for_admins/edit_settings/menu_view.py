from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.for_admins.edit_settings.buttons.hidden_channels import (
    HiddenChannelsMenuButtons,
)
from features.for_admins.edit_settings.buttons.hidden_roles import HiddenRolesMenuButton
from features.for_admins.edit_settings.buttons.main_settings import MainSettingsButton
from features.for_admins.edit_settings.buttons.sys_channels import (
    SystemChannelsMenuButton,
)
from ui.buttons.back_button import BackButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from features.for_admins.edit_settings.services.hidden_channels import (
        HiddenChannelsService,
    )
    from features.for_admins.edit_settings.services.hidden_roles import (
        HiddenRolesService,
    )
    from features.for_admins.edit_settings.services.main_settings.main_service import (
        MainSettingsService,
    )
    from features.for_admins.edit_settings.services.main_settings.role_service import (
        VerificationRoleService,
    )
    from features.for_admins.edit_settings.services.settings_formatter import (
        SettingsFormatter,
    )
    from general_services.other_services.cleanup_service import CleanUpService
    from general_services.translator.translator import Translator
    from ui.button_protection.button_protection_service import ButtonProtectionService


class SettingsMenuView(discord.ui.View):
    def __init__(
        self,
        navigator: Navigator,
        context: NavigationContext,
        main_settings_service: MainSettingsService,
        settings_formatter: SettingsFormatter,
        buttons_protection: ButtonProtectionService,
        hidden_ch_service: HiddenChannelsService,
        hidden_role_service: HiddenRolesService,
        service_for_role: VerificationRoleService,
        cleanup_service: CleanUpService,
        translator: Translator,
        guild_id: int,
    ):
        super().__init__(timeout=60)

        self.add_item(
            MainSettingsButton(
                navigator=navigator,
                context=context,
                main_settings_service=main_settings_service,
                formatter=settings_formatter,
                buttons_protection=buttons_protection,
                service_for_role=service_for_role,
                translator=translator,
                guild_id=guild_id,
            )
        )

        self.add_item(
            SystemChannelsMenuButton(
                navigator=navigator,
                context=context,
                buttons_protection=buttons_protection,
                formatter=settings_formatter,
                translator=translator,
                guild_id=guild_id,
            )
        )

        self.add_item(
            HiddenChannelsMenuButtons(
                navigator=navigator,
                context=context,
                buttons_protection=buttons_protection,
                formatter=settings_formatter,
                hidden_ch_service=hidden_ch_service,
                cleanup_service=cleanup_service,
                translator=translator,
                guild_id=guild_id,
            )
        )

        self.add_item(
            HiddenRolesMenuButton(
                navigator=navigator,
                context=context,
                buttons_protection=buttons_protection,
                formatter=settings_formatter,
                hidden_roles_service=hidden_role_service,
                cleanup_service=cleanup_service,
                translator=translator,
                guild_id=guild_id,
            )
        )

        self.add_item(
            BackButton(navigator=navigator, translator=translator, guild_id=guild_id)
        )
