from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.db_base_service import DBBaseService
from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.settings_storage.settings import SettingsStorage
    from database.db_factory.db_scenario_factory import DBFactory


class VerificationService(DBBaseService):
    def __init__(self, bot: Bot, settings: SettingsStorage, db_factory: DBFactory):
        super().__init__(settings)

        self.bot = bot
        self.settings = settings
        self.db_factory = db_factory

    async def save_message_id(self, message_id: int, guild_id: int) -> None:
        save_message = self.db_factory.for_write_data(
            guild_id=guild_id,
            table_name='settings',
            data={'verification_message_id': message_id}
        )

        await self.update_db_and_cache(
            scenario=save_message,
            guild_id=guild_id
        )

    async def get_verification_channel(self, guild: discord.Guild) -> discord.TextChannel | None:
        channel_id = self.settings.dict_storage.get_value(
            'verification_channel_id',
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild.id
        )

        if not channel_id:
            return None

        channel = guild.get_channel(channel_id)

        if not channel:
            try:
                channel = await self.bot.fetch_channel(channel_id)
            except discord.NotFound:
                return None

        if isinstance(channel, discord.TextChannel):
            return channel

        return None
