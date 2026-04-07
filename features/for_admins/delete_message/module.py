from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .service import DeleteMessageService

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage


@dataclass
class DeleteMessageModule:
    delete_msg_service: DeleteMessageService


def build_delete_msg_module(settings: SettingsStorage) -> DeleteMessageModule:
    delete_msg_service = DeleteMessageService(settings=settings)
    return DeleteMessageModule(delete_msg_service=delete_msg_service)
