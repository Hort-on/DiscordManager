from dataclasses import dataclass

import discord


@dataclass(slots=True)
class AdminMenuParams:
    guild_id: int


@dataclass(slots=True)
class MainMenuParams:
    guild_id: int
    user_id: int
    owner_id: int
