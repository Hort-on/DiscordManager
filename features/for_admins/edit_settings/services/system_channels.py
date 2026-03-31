from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from PIL.ImageCms import isIntentSupported

from database.db_base_service import DBBaseService
from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from core.bot_config import Bot
    from features.auto_moderation.verification.service import VerificationService
    from features.auto_moderation.verification.view_service import VerificationViewService
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage


class SystemChannelsService(DBBaseService):
    def __init__(
            self,
            bot: Bot,
            db_factory: DBFactory,
            settings: SettingsStorage,
            service: VerificationService,
            verification_view_service: VerificationViewService
    ):
        super().__init__(settings)

        self.bot = bot
        self.db_factory = db_factory
        self.settings = settings
        self.service = service
        self.view_service = verification_view_service

    async def save_system_channel(self, guild: discord.Guild, channel_data: dict[str, int]) -> bool:
        write_scenario = self.db_factory.for_write_data(
            guild_id=guild.id,
            table_name='sys_channels',
            data=channel_data
        )

        result = await self.update_db_and_cache(
            scenario=write_scenario,
            guild_id=guild.id
        )

        if not result:
            return False

        if 'verification_channel_id' in channel_data:
            result = self.settings.dict_storage.get_value(
                key='verification',
                target=StorageTarget.SETTINGS,
                guild_id=guild.id,
            )

            if result:
                channel = await self.service.get_verification_channel(guild=guild)
                if not isinstance(channel, discord.TextChannel):
                    return False

                await self.view_service.ensure_single_message(
                    channel=channel,
                    guild_id=guild.id
                )

        return True

    async def delete_channels(self, guild_id: int, values: list[str]) -> bool:
        delete_scenario = self.db_factory.for_cleanup_system_channel(
            guild_id=guild_id,
            channels=values
        )

        result = await self.update_db_and_cache(
            scenario=delete_scenario,
            guild_id=guild_id
        )

        return result

    def build_sys_ch_options(self, guild_id: int) -> list[str]:
        sys_channels = self.settings.dict_storage.get_all(
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild_id
        )

        return [key for key in sorted(sys_channels.keys(), key=lambda item: item[0])]
