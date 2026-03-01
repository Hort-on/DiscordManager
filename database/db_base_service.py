from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage


class DBBaseService:
    def __init__(self, settings: SettingsStorage):
        self.settings = settings

    async def update_db_and_cache(self, scenario, guild_id: int) -> bool:
        result = await scenario.db_proceed()

        if result:
            await self.settings.reload_guild(
                guild_id=guild_id
            )

        return bool(result)
