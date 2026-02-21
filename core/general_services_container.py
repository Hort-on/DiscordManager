from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage
    from database.db_factory.db_scenario_factory import DBFactory
    from database.data_base_model import DB
    from general_services.logger.logger import Logger
    from general_services.other_services.cleanup_service import CleanUpService


@dataclass
class GeneralContainer:
    logger: Logger
    db_connect: DB
    db_factory: DBFactory
    settings: SettingsStorage
    cleanup_service: CleanUpService
