from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from features.for_everyone.birthdays.module import build_birthday_module
from features.for_everyone.randomizer.module import build_randomizer_module
from features.for_everyone.role_manager.module import build_role_manager_module
from features.for_everyone.temp_voice_channel.module import (
    build_temp_voice_channel_module,
)

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from features.for_everyone.birthdays.module import BirthdayForUserModule
    from features.for_everyone.randomizer.module import RandomizerModule
    from features.for_everyone.role_manager.module import RoleManagerModule
    from features.for_everyone.temp_voice_channel.module import TempVoiceChannelModule
    from general_services.translator.translator import Translator


@dataclass
class EveryoneModule:
    birthday_module: BirthdayForUserModule
    randomizer_module: RandomizerModule
    role_manager_module: RoleManagerModule
    temp_voice_channel_module: TempVoiceChannelModule


def build_everyone_module(
    bot: Bot, settings: SettingsStorage, db_factory: DBFactory, translator: Translator
) -> EveryoneModule:
    birthday_module = build_birthday_module(
        bot=bot, settings=settings, db_factory=db_factory, translator=translator
    )

    randomizer_module = build_randomizer_module(settings=settings)

    role_manager_module = build_role_manager_module(settings=settings)
    temp_voice_channel_module = build_temp_voice_channel_module(db_factory=db_factory)

    return EveryoneModule(
        birthday_module=birthday_module,
        randomizer_module=randomizer_module,
        role_manager_module=role_manager_module,
        temp_voice_channel_module=temp_voice_channel_module,
    )
