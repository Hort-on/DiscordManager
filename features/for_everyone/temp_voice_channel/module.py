from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from features.for_everyone.temp_voice_channel.service import TempVoiceChannelService

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory


@dataclass
class TempVoiceChannelModule:
    service: TempVoiceChannelService


def build_temp_voice_channel_module(db_factory: DBFactory) -> TempVoiceChannelModule:
    service = TempVoiceChannelService(db_factory=db_factory)

    return TempVoiceChannelModule(service=service)
