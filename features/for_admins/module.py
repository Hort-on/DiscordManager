from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass


from features.for_admins.delete_message.module import DeleteMessageModule, build_delete_msg_module
from features.for_admins.superusers.module import SuperusersModule, build_superusers_module
from features.for_admins.send_anon_messages.module import SendMessageModule, build_send_anon_msg_module
from features.for_admins.edit_settings.module import EditSettingsModule, build_edit_settings_module


if TYPE_CHECKING:
    from core.bot_config import Bot

    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage

    from general_services.other_services.cleanup_service import CleanUpService

    from features.auto_moderation.verification.check_verification import VerificationService


@dataclass
class AdministrationModule:
    delete_msg_module: DeleteMessageModule
    edit_main_settings_module: EditSettingsModule
    send_message_module: SendMessageModule
    superusers_module: SuperusersModule


def build_admin_module(
        bot: Bot,
        db_factory: DBFactory,
        settings: SettingsStorage,
        cleanup_service: CleanUpService,
        verification_service: VerificationService
) -> AdministrationModule:

    delete_msg_module = build_delete_msg_module(
        settings=settings
    )

    edit_settings_module = build_edit_settings_module(
        bot=bot,
        db_factory=db_factory,
        settings=settings,
        verification_service=verification_service
    )

    send_message_module = build_send_anon_msg_module(
        db_factory=db_factory,
        settings=settings
    )

    superusers_module = build_superusers_module(
        settings=settings,
        db_factory=db_factory,
        cleanup_service=cleanup_service
    )

    return AdministrationModule(
        delete_msg_module=delete_msg_module,
        edit_main_settings_module=edit_settings_module,
        send_message_module=send_message_module,
        superusers_module=superusers_module
    )
