from __future__ import annotations

from typing import TYPE_CHECKING

from database.db_base_service import DBBaseService
from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage


class HiddenRolesService(DBBaseService):
    def __init__(self, db_factory: DBFactory, settings: SettingsStorage):

        super().__init__(settings)

        self.db_factory = db_factory
        self.settings = settings

    async def save_roles(self, guild_id: int, values: list[str]) -> bool:
        role_ids: set[int] = set(int(i) for i in values)

        write_scenario = self.db_factory.for_insert_set(
            guild_id=guild_id,
            values=role_ids,
            table_name='roles',
            key='role_id'
        )

        return await self.update_db_and_cache(
            scenario=write_scenario,
            guild_id=guild_id
        )

    async def delete_roles(self, guild_id: int, values: list[str]) -> bool:
        role_ids: set[int] = set(int(i) for i in values)

        write_scenario = self.db_factory.for_delete_set(
            guild_id=guild_id,
            values=role_ids,
            table_name='roles',
            key='role_id'
        )

        return await self.update_db_and_cache(
            scenario=write_scenario,
            guild_id=guild_id
        )

    def get_hidden_roles(self, guild_id: int) -> set[int]:
        return self.settings.set_storage.for_set_get(
            target=StorageTarget.HIDDEN_ROLES,
            guild_id=guild_id
        )
