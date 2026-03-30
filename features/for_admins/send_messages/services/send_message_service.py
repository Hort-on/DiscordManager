from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.db_base_service import DBBaseService
from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from general_services.translator.translator import Translator


class MessageService(DBBaseService):
    def __init__(self, db_factory: DBFactory, settings: SettingsStorage, translator: Translator):
        super().__init__(settings=settings)
        self.db_factory = db_factory
        self.settings = settings
        self.translator = translator

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

    async def send_message(self, member: discord.Member, message: str) -> None:
        channel_id = self.settings.dict_storage.get_value(
            key=member.id,
            guild_id=member.guild.id,
            target=StorageTarget.CHANNELS_TO_SEND
        )

        if not channel_id:
            return

        channel = member.guild.get_channel(channel_id)
        if not isinstance(channel, discord.TextChannel):
            return

        try:
            await channel.send(message)
        except discord.Forbidden:
            msg = self.translator.t(
                guild_id=member.guild.id,
                section='SEND_MSG',
                key='no_perm_to_send',
                channel_name=channel.name
            )
            await member.send(msg)
        except discord.HTTPException:
            msg = self.translator.t(
                guild_id=member.guild.id,
                section='SEND_MSG',
                key='failed_to_sent',
                channel_name=channel.name
            )
            await member.send(msg)
