from __future__ import annotations

from typing import TYPE_CHECKING

from database.db_base_service import DBBaseService
from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage


class HiddenChannelsService(DBBaseService):
    def __init__(self, db_factory: DBFactory, settings: SettingsStorage):
        super().__init__(settings)

        self.db_factory = db_factory
        self.settings = settings

    async def update_channels_values(self, guild_id: int, values: list[str]) -> bool:
        channel_ids = set(int(item) for item in values)

        write_scenario = self.db_factory.for_insert_set(
            guild_id=guild_id,
            values=channel_ids,
            table_name='hidden_channels',
            key='channel_id'
        )

        result = await self.update_db_and_cache(
            scenario=write_scenario,
            guild_id=guild_id
        )

        return result

    async def delete_channels(self, guild_id: int, values: list[str]) -> bool:
        channel_ids = set(int(item) for item in values)

        delete_scenario = self.db_factory.for_delete_set(
            guild_id=guild_id,
            values=channel_ids,
            table_name='hidden_channels',
            key='channel_id'
        )

        result = await self.update_db_and_cache(
            scenario=delete_scenario,
            guild_id=guild_id
        )

        return result

    def get_hidden_channels(self, guild_id: int) -> set[int]:
        return self.settings.set_storage.for_set_get(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=guild_id
        )
