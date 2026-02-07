from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.container import BotContainer
    from database.settings_storage.settings import SettingsStorage
    from services.factories.db_factory.db_scenario_factory import DBFactory

from database.settings_storage.settings_manager import StorageTarget

from core.container import AppContainer


class CleanUpService:
    def __init__(self):
        container: BotContainer = AppContainer.get()
        self.settings: SettingsStorage = container.settings
        self.db_factory: DBFactory = container.db_factory

    async def clean_up_hidden_channels(self, guild_id: int, values: set[int]) -> str:
        delete = self.db_factory.for_cleanup_hidden_channel(
            guild_id=guild_id,
            channel_ids=values
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

    async def clean_up_system_channels(self, guild_id: int, channels: dict[str, int]) -> str:
        delete = self.db_factory.for_cleanup_system_channel(
            guild_id=guild_id,
            channels=channels
        )

        result = await delete.db_proceed()
        if not result:
            return '⚠️Somethings went wrong, could not delete not found ids'

        self.settings.dict_storage.for_dict_remove(
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild_id,
            keys=[key for key in channels.keys()]
        )

        return f'⚠️{len(channels)} were not found and has been deleted'

    async def clean_up_hidden_roles(self, guild_id: int, role_ids: set[int]) -> str:
        delete = self.db_factory.for_cleanup_hidden_roles(
            guild_id=guild_id,
            role_ids=role_ids
        )

        result = await delete.db_proceed()
        if not result:
            return '⚠️Somethings went wrong, could not delete not found ids'

        self.settings.set_storage.for_set_remove(
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild_id,
            value=role_ids
        )

        return f'⚠️{len(role_ids)} were not found and has been deleted'
