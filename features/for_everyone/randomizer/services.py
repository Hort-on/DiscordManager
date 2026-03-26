from __future__ import annotations

from typing import TYPE_CHECKING

import random

import discord

from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage


class RandomizerService:
    def __init__(self, settings: SettingsStorage):
        self.settings = settings

    @staticmethod
    def build_teams_by_text(members: list[str], teams_quantity: int) -> list[list]:
        random.shuffle(members)

        teams = [[] for _ in range(teams_quantity)]

        for i, member in enumerate(members):
            teams[i % teams_quantity].append(member)

        return teams

    @staticmethod
    def team_by_channel_proceed(members: list[discord.Member], teams_quantity: int) -> list[list]:
        random.shuffle(members)

        teams = [[] for _ in range(teams_quantity)]

        for i, member in enumerate(members):
            teams[i % teams_quantity].append(member.display_name)

        return teams

    def get_hidden_channels(self, guild_id: int) -> set[int]:
        return self.settings.set_storage.for_set_get(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=guild_id
        )
