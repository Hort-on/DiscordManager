from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.db_base_service import DBBaseService
from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage


class MessageService(DBBaseService):
    def __init__(self, db_factory: DBFactory, settings: SettingsStorage):
        super().__init__(settings)

        self.db_factory = db_factory
        self.settings = settings

    def get_channels(self, guild: discord.Guild) -> list[discord.SelectOption]:
        channels = guild.text_channels

        hidden_channels = self.settings.set_storage.for_set_get(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=guild.id
        )

        return [discord.SelectOption(
            label=channel.name,
            value=str(channel.id)
        )
            for channel in channels if channel.id not in hidden_channels
        ]

    async def save_channel(self, guild_id: int, user_id: int, channel_id: int) -> bool:
        write_scenario = self.db_factory.for_write_data(
            guild_id=guild_id,
            table_name='channels_to_send',
            data={
                'guild_id': guild_id,
                'user_id': user_id,
                'channel_id': channel_id
            }
        )

        result = await self.update_db_and_cache(
            scenario=write_scenario,
            guild_id=guild_id
        )

        return result
