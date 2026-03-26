from __future__ import annotations

from dataclasses import dataclass

from typing import TYPE_CHECKING

from features.for_everyone.birthdays.service import BirthdayService

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from general_services.translator.translator import Translator


@dataclass
class BirthdayForUserModule:
    service: BirthdayService


def build_birthday_module(
        bot: Bot,
        settings: SettingsStorage,
        db_factory: DBFactory,
        translator: Translator
) -> BirthdayForUserModule:
    service = BirthdayService(
        bot=bot,
        settings=settings,
        db_factory=db_factory,
        translator=translator
    )

    return BirthdayForUserModule(service=service)
