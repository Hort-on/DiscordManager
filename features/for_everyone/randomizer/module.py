from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass

from features.for_everyone.randomizer.services import RandomizerService

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage


@dataclass
class RandomizerModule:
    service: RandomizerService


def build_randomizer_module(settings: SettingsStorage) -> RandomizerModule:
    service = RandomizerService(settings=settings)
    return RandomizerModule(service=service)
