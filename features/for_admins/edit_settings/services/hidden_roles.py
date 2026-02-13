from __future__ import annotations

from typing import TYPE_CHECKING

from database.settings_storage.settings_manager import StorageTarget

from ui.embed_constructor.embed_constructor import SuccessEmbed, ErrorEmbed

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage


class HiddenRolesService:
    def __init__(
            self,
            db_factory: DBFactory,
            settings: SettingsStorage,
    ):

        self.db_factory = db_factory
        self.settings = settings

    async def save_roles(self, guild_id: int, values: list[str]) -> bool:
        role_ids: set[int] = set(int(i) for i in values)

        write = self.db_factory.for_insert_set(
            guild_id=guild_id,
            values=role_ids,
            table_name='roles',
            key='role_id'
        )

        result = await write.db_proceed()
        if not result:
            return False

        self.settings.set_storage.for_set_add(
            target=StorageTarget.HIDDEN_ROLES,
            guild_id=guild_id,
            value=role_ids
        )

        return True

    async def delete_roles(self, guild_id: int, values: list[str]) -> bool:
        role_ids: set[int] = set(int(i) for i in values)

        write = self.db_factory.for_delete_set(
            guild_id=guild_id,
            values=role_ids,
            table_name='roles',
            key='role_id'
        )

        result = await write.db_proceed()
        if not result:
            return False

        self.settings.set_storage.for_set_remove(
            target=StorageTarget.HIDDEN_ROLES,
            guild_id=guild_id,
            value=values
        )

        return True

    def get_hidden_roles(self, guild_id: int) -> set[int]:
        return self.settings.set_storage.for_set_get(
            target=StorageTarget.HIDDEN_ROLES,
            guild_id=guild_id
        )
