from __future__ import annotations

from typing import TYPE_CHECKING

from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage


class HiddenChannelsService:
    def __init__(
            self,
            db_factory: DBFactory,
            settings: SettingsStorage,
    ):

        self.db_factory = db_factory
        self.settings = settings

    async def update_channels_values(self, guild_id: int, values: list[str]) -> bool:
        channel_ids = set(int(item) for item in values)

        update = self.db_factory.for_insert_set(
            guild_id=guild_id,
            values=channel_ids,
            table_name='hidden_channels',
            key='channel_id'
        )

        result = await update.db_proceed()
        if not result:
            return False

        self.settings.set_storage.for_set_add(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=guild_id,
            value=channel_ids
        )

        return True

    async def delete_channels(self, guild_id: int, values: list[str]) -> bool:
        channel_ids = set(int(item) for item in values)

        delete = self.db_factory.for_delete_set(
            guild_id=guild_id,
            values=channel_ids,
            table_name='hidden_channels',
            key='channel_id'
        )

        result = await delete.db_proceed()
        if not result:
            return False

        self.settings.set_storage.for_set_remove(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=guild_id,
            value=values
        )

        return True

    def get_hidden_channels(self, guild_id: int) -> set[int]:
        return self.settings.set_storage.for_set_get(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=guild_id
        )
