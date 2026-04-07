from __future__ import annotations

from typing import TYPE_CHECKING

from database.db_base_service import DBBaseService
from database.settings_storage.settings_manager import StorageTarget

from .results import AvailableUsers

if TYPE_CHECKING:
    import discord

    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from general_services.other_services.cleanup_service import CleanUpService
    from general_services.translator.translator import Translator


class SuperusersService(DBBaseService):
    def __init__(
        self,
        settings: SettingsStorage,
        db_factory: DBFactory,
        cleanup_service: CleanUpService,
        translator: Translator,
    ):
        super().__init__(settings)

        self.settings = settings
        self.db_factory = db_factory
        self.cleanup_service = cleanup_service
        self.translator = translator

    async def add_superusers(self, guild_id: int, user_ids: set[int]) -> bool:
        if not user_ids:
            return False

        scenario = self.db_factory.for_insert_set(
            guild_id=guild_id, values=user_ids, table_name="super_users", key="user_id"
        )

        return await self.update_db_and_cache(scenario=scenario, guild_id=guild_id)

    async def delete_superusers(self, guild_id: int, values: list[str]) -> bool:
        user_ids = {int(user_id) for user_id in values}

        scenario = self.db_factory.for_delete_set(
            guild_id=guild_id, values=user_ids, table_name="super_users", key="user_id"
        )

        return await self.update_db_and_cache(scenario=scenario, guild_id=guild_id)

    def get_current_superusers(self, guild_id: int) -> set[int]:
        return self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS, guild_id=guild_id
        )

    async def get_superusers_for_deletion(
        self, guild: discord.Guild, client: discord.Client
    ) -> tuple[dict[int, str], str | None]:

        users = self._get_available_users(guild=guild)

        if not users.not_found_ids:
            return users.available_users, None

        cleaned = await self.cleanup_service.cleanup_superusers(
            guild_id=guild.id, user_ids=users.not_found_ids
        )

        if not cleaned:
            msg = await self._build_not_found_message(
                user_ids=users.not_found_ids, client=client, guild_id=guild.id
            )
            return users.available_users, msg

        msg = await self._build_cleaned_message(
            user_ids=users.not_found_ids, client=client, guild_id=guild.id
        )

        return users.available_users, msg

    def _get_available_users(self, guild: discord.Guild) -> AvailableUsers:
        superusers = self.get_current_superusers(guild_id=guild.id)

        available: dict[int, str] = {}
        not_found: set[int] = set()

        for user_id in superusers:
            member = guild.get_member(user_id)

            if member:
                display = member.display_name
                global_name = member.global_name or member.name
                available[user_id] = f"{display} ({global_name})"
            else:
                not_found.add(user_id)

        return AvailableUsers(available_users=available, not_found_ids=not_found)

    async def _build_not_found_message(
        self, user_ids: set[int], client: discord.Client, guild_id: int
    ) -> str:
        msg = self.translator.t(
            guild_id=guild_id, section="SUPERUSERS", key="not_found_users"
        )
        lines = [msg, "-" * 40]

        for user_id in user_ids:
            user = await client.fetch_user(user_id)
            name = user.global_name or user.name
            lines.append(f"🔸 {name}")

        return "\n".join(lines)

    async def _build_cleaned_message(
        self, user_ids: set[int], client: discord.Client, guild_id: int
    ) -> str:
        msg = self.translator.t(
            guild_id=guild_id, section="SUPERUSERS", key="not_found_users"
        )
        lines = [msg, "-" * 40]

        for user_id in user_ids:
            user = await client.fetch_user(user_id)
            name = user.global_name or user.name
            lines.append(f"🔸 {name}")

        return "\n".join(lines)
