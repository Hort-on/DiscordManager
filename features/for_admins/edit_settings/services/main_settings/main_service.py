from __future__ import annotations

from typing import TYPE_CHECKING, Any

import discord

from database.db_base_service import DBBaseService
from database.settings_storage.settings_manager import StorageTarget

from features.auto_moderation.verification.service import VerificationService

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from features.auto_moderation.verification.view_service import VerificationViewService


class MainSettingsService(DBBaseService):
    def __init__(
            self,
            bot: Bot,
            db_factory: DBFactory,
            settings: SettingsStorage,
            verification_service: VerificationService,
            verification_view_service: VerificationViewService
    ):
        super().__init__(settings)

        self.bot = bot
        self.db_factory = db_factory
        self.settings = settings
        self.service = verification_service
        self.view_service = verification_view_service

    def get_main_settings(self, guild_id: int) -> dict[str, Any]:
        return self.settings.dict_storage.get_all(
            target=StorageTarget.SETTINGS,
            guild_id=guild_id
        )

    def is_setting_enabled(self, guild_id: int, config_key: str) -> bool:
        result = self.settings.dict_storage.get_value(
            key=config_key,
            target=StorageTarget.SETTINGS,
            guild_id=guild_id,
        )

        return bool(result)

    async def save_new_value(self, guild: discord.Guild, config_key: str) -> bool:
        current_value = self.settings.dict_storage.get_value(
            key=config_key,
            target=StorageTarget.SETTINGS,
            guild_id=guild.id,
        )

        new_value = not current_value

        if config_key == 'verification' and new_value:
            channel = await self.service.get_verification_channel(guild=guild)
            if channel:
                await self.view_service.ensure_single_message(
                    channel=channel,
                    guild_id=guild.id
                )
        elif config_key == 'verification' and not new_value:
            await self._cleanup_verification_message(guild=guild)

        write_scenario = self.db_factory.for_write_data(
            guild_id=guild.id,
            table_name='settings',
            data={config_key: new_value}
        )

        result = await self.update_db_and_cache(
            scenario=write_scenario,
            guild_id=guild.id
        )

        return bool(result)

    async def _cleanup_verification_message(self, guild) -> None:
        channel_id = self.settings.dict_storage.get_value(
            key='verification_channel_id',
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild.id
        )

        if not channel_id:
            return

        channel = guild.get_channel(channel_id)
        if not channel:
            return

        msg_id = self.settings.dict_storage.get_value(
            key='verification_message_id',
            target=StorageTarget.SETTINGS,
            guild_id=guild.id
        )

        if not msg_id:
            return

        try:
            message = await channel.fetch_message(msg_id)
            await message.delete()
        except discord.NotFound:
            pass

        delete_msg = self.db_factory.for_delete_set(
            guild_id=guild.id,
            values=msg_id,
            table_name='settings',
            key='verification_message_id'
        )

        await self.update_db_and_cache(
            scenario=delete_msg,
            guild_id=guild.id
        )

    async def save_new_language(self, guild_id: int) -> bool:
        result = self.settings.dict_storage.get_value(
            key='language',
            target=StorageTarget.SETTINGS,
            guild_id=guild_id
        )

        save_lang = self.db_factory.for_write_data(
            guild_id=guild_id,
            table_name='settings',
            data={'language': f'{'uk' if result == 'en' else 'en'}'}
        )

        result = await self.update_db_and_cache(
            scenario=save_lang,
            guild_id=guild_id
        )

        return bool(result)
