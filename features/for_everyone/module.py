from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass


from features.for_everyone.birthdays.module import build_birthday_module
from features.for_everyone.randomizer.module import build_randomizer_module

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.settings_storage.settings import SettingsStorage
    from database.db_factory.db_scenario_factory import DBFactory
    from features.for_everyone.birthdays.module import BirthdayForUserModule
    from features.for_everyone.randomizer.module import RandomizerModule


@dataclass
class EveryoneModule:
    birthday_module: BirthdayForUserModule
    randomizer_module: RandomizerModule


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

    randomizer_module = build_randomizer_module(
        settings=settings
    )

    return EveryoneModule(
        birthday_module=birthday_module,
        randomizer_module=randomizer_module
    )
