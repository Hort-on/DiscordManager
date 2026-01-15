import discord

import asyncio

from typing import Optional

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

from services.factories.db_factory.db_scenario_factory import DBScenarioFactory


class GetSuperusersList:
    def __init__(
        self,
        settings: SettingsStorage,
        db_factory: DBScenarioFactory,
    ):
        self.settings = settings
        self.db_factory = db_factory

    def get_display(self, guild: discord.Guild) -> Optional[str]:
        user_ids = self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=guild.id
        )

        if not user_ids:
            return None

        return self._format_members(guild=guild, user_ids=user_ids)

    def _format_members(
        self,
        guild: discord.Guild,
        user_ids: set[int]
    ) -> str:
        names = ['The list of current users:']
        not_found_users: set[int] = set()

        for user_id in user_ids:
            member = guild.get_member(user_id)

            if not member:
                not_found_users.add(user_id)
                continue

            names.append(member.display_name)

        if not_found_users:
            asyncio.create_task(self._clean_up_not_found(
                guild_id=guild.id,
                not_found_users=not_found_users)
            )

        return '\n-> '.join(names)

    async def _clean_up_not_found(self, guild_id: int, not_found_users: set[int]):
        self.settings.set_storage.for_set_remove(
            target=StorageTarget.SUPERUSERS,
            guild_id=guild_id,
            value=not_found_users
        )

        cleanup_scenario = self.db_factory.for_remove_user(
            guild_id=guild_id,
            user_ids=not_found_users
        )

        await cleanup_scenario.db_proceed()
