from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from features.auto_moderation.verification.view_service import VerificationViewService

from .services.hidden_channels import HiddenChannelsService
from .services.hidden_roles import HiddenRolesService
from .services.main_settings.main_service import MainSettingsService
from .services.main_settings.role_service import VerificationRoleService
from .services.settings_formatter import SettingsFormatter
from .services.system_channels import SystemChannelsService

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from features.auto_moderation.verification.service import VerificationService
    from general_services.other_services.cleanup_service import CleanUpService
    from general_services.translator.translator import Translator


@dataclass
class EditSettingsModule:
    hidden_channel_service: HiddenChannelsService
    hidden_roles_service: HiddenRolesService
    system_channels_service: SystemChannelsService
    formatter: SettingsFormatter
    main_settings_service: MainSettingsService
    verification_role_service: VerificationRoleService


def build_edit_settings_module(
    bot: Bot,
    db_factory: DBFactory,
    settings: SettingsStorage,
    verification_service: VerificationService,
    verification_view_service: VerificationViewService,
    cleanup_service: CleanUpService,
    translator: Translator,
) -> EditSettingsModule:

    hidden_channel_service = HiddenChannelsService(
        db_factory=db_factory, settings=settings
    )

    hidden_roles_service = HiddenRolesService(db_factory=db_factory, settings=settings)

    system_channels_service = SystemChannelsService(
        bot=bot,
        db_factory=db_factory,
        settings=settings,
        service=verification_service,
        verification_view_service=verification_view_service,
    )

    formatter = SettingsFormatter(
        settings=settings,
        db_factory=db_factory,
        cleanup_service=cleanup_service,
        translator=translator,
    )

    main_settings_service = MainSettingsService(
        bot=bot,
        db_factory=db_factory,
        settings=settings,
        verification_service=verification_service,
        verification_view_service=verification_view_service,
    )

    verification_role_service = VerificationRoleService(
        settings=settings, db_factory=db_factory
    )

    return EditSettingsModule(
        hidden_channel_service=hidden_channel_service,
        hidden_roles_service=hidden_roles_service,
        system_channels_service=system_channels_service,
        formatter=formatter,
        main_settings_service=main_settings_service,
        verification_role_service=verification_role_service,
    )
