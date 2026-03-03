from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass

from features.for_admins.send_messages.services.send_message_service import MessageService

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from features.for_admins.send_messages.services.send_rules_service import RulesService


@dataclass
class SendMessageModule:
    send_message_service: MessageService
    rules_service: RulesService


def build_messages_module(
        db_factory: DBFactory,
        settings: SettingsStorage,
        rules_service: RulesService
) -> SendMessageModule:
    send_message_service = MessageService(
        db_factory=db_factory,
        settings=settings
    )
    return SendMessageModule(
        send_message_service=send_message_service,
        rules_service=rules_service
    )
