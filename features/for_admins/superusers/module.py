from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass

from .services import SuperusersService
from .formatter import SuperusersFormatter

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from general_services.other_services.cleanup_service import CleanUpService
    from general_services.translator.translator import Translator


@dataclass
class SuperusersModule:
    superusers_service: SuperusersService
    superusers_formatter: SuperusersFormatter


def build_superusers_module(
        settings: SettingsStorage,
        db_factory: DBFactory,
        cleanup_service: CleanUpService,
        translator: Translator
) -> SuperusersModule:
    superusers_service = SuperusersService(
        settings=settings,
        db_factory=db_factory,
        cleanup_service=cleanup_service,
        translator=translator
    )

    superusers_formatter = SuperusersFormatter(
        settings=settings,
        translator=translator
    )

    return SuperusersModule(
        superusers_service=superusers_service,
        superusers_formatter=superusers_formatter
    )
