from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass


from features.for_everyone.birthdays.module import build_birthday_module

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.settings_storage.settings import SettingsStorage
    from database.db_factory.db_scenario_factory import DBFactory
    from features.for_everyone.birthdays.module import BirthdayForUserModule


@dataclass
class EveryoneModule:
    birthday_module: BirthdayForUserModule


def build_everyone_module(
        bot: Bot,
        settings: SettingsStorage,
        db_factory: DBFactory
) -> EveryoneModule:
    birthday_module = build_birthday_module(
        bot=bot,
        settings=settings,
        db_factory=db_factory
    )

    return EveryoneModule(
        birthday_module=birthday_module
    )
