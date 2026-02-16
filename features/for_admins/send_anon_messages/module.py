from __future__ import annotations

from typing import TYPE_CHECKING

from features.for_admins.send_anon_messages.service import SendAnonMessageService

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage


def build(db_factory: DBFactory, settings: SettingsStorage) -> SendAnonMessageService:
    return SendAnonMessageService(
        db_factory=db_factory,
        settings=settings
    )
