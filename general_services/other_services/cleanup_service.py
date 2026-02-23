from __future__ import annotations

from typing import TYPE_CHECKING

from database.db_base_service import DBBaseService

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage
    from database.db_factory.db_scenario_factory import DBFactory


class CleanUpService(DBBaseService):
    def __init__(self, settings: SettingsStorage, db_factory: DBFactory):
        super().__init__(settings)

        self.settings = settings
        self.db_factory = db_factory

    async def clean_up_hidden_channels(self, guild_id: int, values: set[int]) -> str:
        delete_scenario = self.db_factory.for_delete_set(
            guild_id=guild_id,
            values=values,
            table_name='hidden_channels',
            key='channel_id'
        )

        result = await self.update_db_and_cache(
            scenario=delete_scenario,
            guild_id=guild_id
        )

        if not result:
            return '⚠️Somethings went wrong, could not delete not found ids'

        return f'⚠️{len(values)} were not found and has been deleted'

    async def clean_up_system_channels(self, guild_id: int, channels: list[str]) -> str:
        delete_scenario = self.db_factory.for_cleanup_system_channel(
            guild_id=guild_id,
            channels=channels
        )

        result = await self.update_db_and_cache(
            scenario=delete_scenario,
            guild_id=guild_id
        )

        if not result:
            return '⚠️Somethings went wrong, could not delete not found ids'

        return f'⚠️{len(channels)} were not found and has been deleted'

    async def clean_up_hidden_roles(self, guild_id: int, role_ids: set[int]) -> str:
        delete_scenario = self.db_factory.for_delete_set(
            guild_id=guild_id,
            values=role_ids,
            table_name='roles',
            key='role_id'
        )

        result = await self.update_db_and_cache(
            scenario=delete_scenario,
            guild_id=guild_id
        )

        if not result:
            return '⚠️Somethings went wrong, could not delete not found ids'

        return f'⚠️{len(role_ids)} were not found and has been deleted'

    async def cleanup_superusers(self, guild_id: int, user_ids: set[int]) -> bool:
        delete_scenario = self.db_factory.for_cleanup_user(
            guild_id=guild_id,
            user_ids=user_ids
        )

        result = await self.update_db_and_cache(
            scenario=delete_scenario,
            guild_id=guild_id
        )

        return result
