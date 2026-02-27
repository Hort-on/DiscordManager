from __future__ import annotations

from typing import TYPE_CHECKING, Any

from database.db_base_service import DBBaseService
from database.settings_storage.settings_manager import StorageTarget

from features.auto_moderation.verification.service import VerificationService

if TYPE_CHECKING:
    from core.bot_config import Bot

    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage


class MainSettingsService(DBBaseService):
    def __init__(
            self,
            bot: Bot,
            db_factory: DBFactory,
            settings: SettingsStorage,
            verification_service: VerificationService
    ):
        super().__init__(settings)

        self.bot = bot
        self.db_factory = db_factory
        self.settings = settings
        self.service = verification_service

    def get_main_settings(self, guild_id: int) -> dict[str, Any]:
        return self.settings.dict_storage.for_dict_get(
            target=StorageTarget.SETTINGS,
            guild_id=guild_id
        )

    def is_setting_enabled(self, guild_id: int, config_key: str) -> bool:
        result = self.settings.dict_storage.for_dict_get(
            config_key,
            target=StorageTarget.SETTINGS,
            guild_id=guild_id,
        )

        return bool(result.get(config_key))

    async def handle_setting_update(self, guild_id: int, config_key: str) -> bool:
        if config_key == 'verification':

            if not self.is_setting_enabled(
                    guild_id=guild_id,
                    config_key=config_key
            ):
                await self._clean_up_verification(guild_id=guild_id)

            # await self.service.

        return await self._save_new_value(
            guild_id=guild_id,
            config_key=config_key
        )

    async def save_new_role(self, guild_id: int, role_id: int) -> bool:
        write_scenario = self.db_factory.for_write_data(
            guild_id=guild_id,
            table_name='settings',
            data={'verification_role_id': role_id}
        )

        result = await self.update_db_and_cache(
            scenario=write_scenario,
            guild_id=guild_id
        )

        return result

    async def _save_new_value(self, guild_id: int, config_key: str) -> bool:
        current_value = self.settings.dict_storage.for_dict_get(
            config_key,
            target=StorageTarget.SETTINGS,
            guild_id=guild_id,
        )

        current = current_value.get(config_key, False)
        new_value = not current

        write_scenario = self.db_factory.for_write_data(
            guild_id=guild_id,
            table_name='settings',
            data={config_key: new_value}
        )

        result = await self.update_db_and_cache(
            scenario=write_scenario,
            guild_id=guild_id
        )

        return result

    async def _clean_up_verification(self, guild_id: int) -> None:
        delete_channel_scenario = self.db_factory.for_cleanup_system_channel(
            guild_id=guild_id,
            channels=['verification_channel_id']
        )

        await self.update_db_and_cache(
            scenario=delete_channel_scenario,
            guild_id=guild_id
        )

        delete_role_scenario = self.db_factory.for_cleanup_role_delete(
            guild_id=guild_id
        )

        await self.update_db_and_cache(
            scenario=delete_role_scenario,
            guild_id=guild_id
        )
