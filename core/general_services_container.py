from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.data_base_model import DB
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from general_services.logger.logger import Logger
    from general_services.other_services.cleanup_service import CleanUpService
    from general_services.translator.translator import Translator
    from ui.button_protection.button_protection_service import ButtonProtectionService


@dataclass
class GeneralContainer:
    logger: Logger
    db_connect: DB
    db_factory: DBFactory
    settings: SettingsStorage
    translator: Translator
    cleanup_service: CleanUpService
    button_protection: ButtonProtectionService
