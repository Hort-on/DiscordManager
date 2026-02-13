from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage
    from database.db_factory.db_scenario_factory import DBFactory

from database.settings_storage.settings_manager import StorageTarget


class CleanUpService:
    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBFactory
    ):
        self.settings = settings
        self.db_factory = db_factory

    async def clean_up_hidden_channels(self, guild_id: int, values: set[int]) -> str:
        delete = self.db_factory.for_delete_set(
            guild_id=guild_id,
            values=values,
            table_name='hidden_channels',
            key='channel_id'
        )

        result = await delete.db_proceed()
        if not result:
            return '⚠️Somethings went wrong, could not delete not found ids'

        self.settings.set_storage.for_set_remove(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=guild_id,
            value=values
        )

        return f'⚠️{len(values)} were not found and has been deleted'

    async def clean_up_system_channels(self, guild_id: int, channels: list[str]) -> str:
        delete = self.db_factory.for_cleanup_system_channel(
            guild_id=guild_id,
            channels=channels
        )

        result = await delete.db_proceed()
        if not result:
            return '⚠️Somethings went wrong, could not delete not found ids'

        channel_keys = [ch for ch in channels]

        self.settings.dict_storage.for_dict_update(
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild_id,
            data={key: None for key in channel_keys}
        )

        return f'⚠️{len(channels)} were not found and has been deleted'

    async def clean_up_hidden_roles(self, guild_id: int, role_ids: set[int]) -> str:
        delete = self.db_factory.for_delete_set(
            guild_id=guild_id,
            values=role_ids,
            table_name='roles',
            key='role_id'
        )

        result = await delete.db_proceed()
        if not result:
            return '⚠️Somethings went wrong, could not delete not found ids'

        self.settings.set_storage.for_set_remove(
            target=StorageTarget.HIDDEN_ROLES,
            guild_id=guild_id,
            value=role_ids
        )

        return f'⚠️{len(role_ids)} were not found and has been deleted'
