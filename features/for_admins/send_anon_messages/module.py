from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass

from features.for_admins.send_anon_messages.service import SendAnonMessageService

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage


@dataclass
class SendMessageModule:
    send_message_service: SendAnonMessageService


def build_send_anon_msg_module(db_factory: DBFactory, settings: SettingsStorage) -> SendMessageModule:
    send_message_service = SendAnonMessageService(
        db_factory=db_factory,
        settings=settings
    )
    return SendMessageModule(
        send_message_service=send_message_service
    )
