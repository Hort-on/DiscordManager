from __future__ import annotations

from typing import TYPE_CHECKING

from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from features.auto_moderation.verification.check_verification import CheckVerification
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from core.bot_config import Bot


class SystemChannelsService:
    def __init__(
            self,
            bot: Bot,
            db_factory: DBFactory,
            settings: SettingsStorage,
    ):
        self.bot = bot
        self.db_factory = db_factory
        self.settings = settings

    async def save_system_channel(self, guild_id: int, channel_data: dict[str, int]) -> bool:
        write = self.db_factory.for_write_data(
            guild_id=guild_id,
            table_name='sys_channels',
            data=channel_data
        )

        result = await write.db_proceed()

        if not result:
            return False

        self.settings.dict_storage.for_dict_update(
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild_id,
            data=channel_data
        )

        if 'verification_channel_id' in channel_data:
            await self._check_if_verification(guild_id=guild_id)

        return True

    async def _check_if_verification(self, guild_id: int):
        verify_status = self.settings.dict_storage.for_dict_get(
            'verification',
            target=StorageTarget.SETTINGS,
            guild_id=guild_id
        )

        if verify_status:
            verify_service = CheckVerification(
                settings=self.settings,
                bot=self.bot
            )

            await verify_service.prepare()

    async def delete_channels(self, guild_id: int, values: list[str]) -> bool:
        delete = self.db_factory.for_cleanup_system_channel(
            guild_id=guild_id,
            channels=values
        )

        result = await delete.db_proceed()
        if not result:
            return False

        channel_keys = [ch for ch in values]

        self.settings.dict_storage.for_dict_update(
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild_id,
            data={key: None for key in channel_keys}
        )

        return True

    def build_sys_ch_options(self, guild_id: int) -> list[str]:
        sys_channels = self.settings.dict_storage.for_dict_get(
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild_id
        )

        return [key for key in sorted(sys_channels.keys(), key=lambda item: item[0])]
