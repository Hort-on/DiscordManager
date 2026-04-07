from __future__ import annotations

from typing import TYPE_CHECKING

from database.db_base_service import DBBaseService
from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage


class VerificationRoleService(DBBaseService):
    def __init__(self, settings: SettingsStorage, db_factory: DBFactory):
        super().__init__(settings=settings)

        self.settings = settings
        self.db_factory = db_factory

    def get_hidden_roles(self, guild_id: int) -> set:
        return self.settings.set_storage.for_set_get(
            target=StorageTarget.HIDDEN_ROLES, guild_id=guild_id
        )

    async def save_role(self, guild_id: int, role_id: int) -> bool:
        write_scenario = self.db_factory.for_write_data(
            guild_id=guild_id,
            table_name="settings",
            data={"verification_role_id": role_id},
        )

        result = await self.update_db_and_cache(
            scenario=write_scenario, guild_id=guild_id
        )

        return bool(result)
