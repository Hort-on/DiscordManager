from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass

if TYPE_CHECKING:
    from features.for_admins.send_messages.services.send_rules_service import RulesService
    from features.for_admins.send_messages.services.send_message_service import MessageService


@dataclass
class SendMessageModule:
    send_message_service: MessageService
    rules_service: RulesService


def build_messages_module(rules_service: RulesService, send_message_service: MessageService) -> SendMessageModule:
    return SendMessageModule(
        send_message_service=send_message_service,
        rules_service=rules_service
    )
