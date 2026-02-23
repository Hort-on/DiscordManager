from __future__ import annotations

from typing import TYPE_CHECKING

from database.db_base_service import DBBaseService
from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from core.bot_config import Bot
    from features.auto_moderation.verification.service import VerificationService
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage


class SystemChannelsService(DBBaseService):
    def __init__(
            self,
            bot: Bot,
            db_factory: DBFactory,
            settings: SettingsStorage,
            service: VerificationService
    ):
        super().__init__(settings)

        self.bot = bot
        self.db_factory = db_factory
        self.settings = settings
        self.service = service

    async def save_system_channel(self, guild_id: int, channel_data: dict[str, int]) -> bool:
        write_scenario = self.db_factory.for_write_data(
            guild_id=guild_id,
            table_name='sys_channels',
            data=channel_data
        )

        result = await self.update_db_and_cache(
            scenario=write_scenario,
            guild_id=guild_id
        )

        if not result:
            return False

        if 'verification_channel_id' in channel_data:
            await self._check_if_verification(guild_id=guild_id)

        return True

    async def _check_if_verification(self, guild_id: int):
        verify_status = self.settings.dict_storage.for_dict_get(
            'verification',
            target=StorageTarget.SETTINGS,
            guild_id=guild_id
        )

        if bool(verify_status):
            await self.service.prepare()

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
        sys_channels = self.settings.dict_storage.for_dict_get(
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild_id
        )

        return [key for key in sorted(sys_channels.keys(), key=lambda item: item[0])]
