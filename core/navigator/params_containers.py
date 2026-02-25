from dataclasses import dataclass

import discord


@dataclass(slots=True)
class AdminMenuParams:
    guild_id: int


@dataclass(slots=True)
class MainMenuParams:
    guild: discord.Guild
    user_id: int
