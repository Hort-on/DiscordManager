from __future__ import annotations

from typing import TYPE_CHECKING

from .service import DeleteMessageService

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage


def build(settings: SettingsStorage) -> DeleteMessageService:
    return DeleteMessageService(
        settings=settings
    )
