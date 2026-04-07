from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.bot_config import Bot
from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage


class RulesService:
    def __init__(self, bot: Bot, settings: SettingsStorage):
        self.bot = bot
        self.settings = settings

        self.active_sessions: dict[int, int] = {}

    def get_verification_channel(self, guild_id: int) -> int | None:
        channel_id = self.settings.dict_storage.get_value(
            key="verification_channel_id",
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild_id,
        )

        return channel_id

    async def send_message(self, message: str, user_id: int) -> None:
        if user_id not in self.active_sessions:
            return

        guild_id = self.active_sessions.get(user_id)
        if not guild_id:
            return

        channel_id = self.get_verification_channel(guild_id=guild_id)
        if not channel_id:
            return

        guild = self.bot.get_guild(guild_id)
        if not guild:
            return

        channel = guild.get_channel(channel_id)

        if not channel:
            try:
                channel = await self.bot.fetch_channel(channel_id)
            except discord.NotFound:
                return

        embed = discord.Embed(
            title="📜 Server rules", colour=discord.Colour.blue(), description=message
        )

        await channel.send(embed=embed)

        self.active_sessions.pop(user_id, None)
