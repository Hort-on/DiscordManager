from __future__ import annotations

from dataclasses import dataclass

from typing import TYPE_CHECKING

from features.for_everyone.birthdays.service import BirthdayService

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage


@dataclass
class BirthdayForUserModule:
    service: BirthdayService


def build_birthday_module(
        bot: Bot,
        settings: SettingsStorage,
        db_factory: DBFactory
) -> BirthdayForUserModule:
    service = BirthdayService(
        bot=bot,
        settings=settings,
        db_factory=db_factory
    )

    return BirthdayForUserModule(
        service=service
    )
