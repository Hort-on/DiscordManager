from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.db_base_service import DBBaseService
from database.settings_storage.settings_manager import StorageTarget

from general_services.other_services.get_member_by_name import get_member_by_name

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from general_services.other_services.cleanup_service import CleanUpService


class SuperusersService(DBBaseService):
    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBFactory,
            cleanup_service: CleanUpService
    ):
        super().__init__(settings)

        self.settings = settings
        self.db_factory = db_factory
        self.cleanup_service = cleanup_service

    # ================================= METHODS FOR ADD BUTTON =================================
    async def prepare_users_for_addition(
            self,
            guild: discord.Guild,
            user_names: str
    ) -> dict[str, str]:
        not_found_users: list[str] = []
        found_users: dict[int, str] = {}
        in_superusers: dict[int, str] = {}

        superusers = self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=guild.id
        )

        usernames = [name.strip() for name in user_names.split(',')]

        for username in usernames:
            member = get_member_by_name(
                guild=guild,
                username=username
            )

            if member is None:
                not_found_users.append(username)
                continue

            if member.id in superusers:
                in_superusers[member.id] = member.display_name
                continue

            found_users[member.id] = username

        return await self._validate_users(
            guild=guild,
            found_users=found_users,
            not_found_result=not_found_users,
            in_superusers=in_superusers
        )

    async def _validate_users(
            self,
            guild: discord.Guild,
            found_users: dict[int, str],
            not_found_result: list[str],
            in_superusers: dict[int, str]
    ) -> dict[str, str]:

        embeds_result: dict[str, str] = {}
        if found_users:
            added_users: list[str] = ['Added superusers:', f'{'-' * 20}']

            for user_id in found_users.keys():
                member = guild.get_member(user_id)
                name = member.display_name
                added_users.append(f'🔸 {name}')

            embeds_result['success_embed'] = '\n'.join(added_users)

        if not_found_result:
            not_found_users: list[str] = ['Not found members:', f'{'-' * 22}',
                                          '\n'.join([f'❗ {name}' for name in not_found_result])]

            embeds_result['warning_embed'] = '\n'.join(not_found_users)

        if in_superusers:
            already_super: list[str] = ['These members are already superusers:', f'{'-' * 37}',
                                        '\n'.join([f'🔸 {name}' for name in in_superusers.values()])]

            embeds_result['info_embed'] = '\n'.join(already_super)

        return await self._save_users(
            embeds_result=embeds_result,
            guild_id=guild.id,
            user_ids=set(u_id for u_id in found_users.keys()),
            found=bool(found_users)
        )

    async def _save_users(
            self,
            embeds_result: dict[str, str],
            guild_id: int,
            user_ids: set[int],
            found: bool
    ) -> dict[str, str]:
        if found:
            write_scenario = self.db_factory.for_insert_set(
                guild_id=guild_id,
                values=user_ids,
                table_name='super_users',
                key='user_id'
            )

            result = await self.update_db_and_cache(
                scenario=write_scenario,
                guild_id=guild_id
            )

            if not result:
                embeds_result['error_embed'] = 'Something went wrong, please try again later.'

        return embeds_result

    # ================================= METHODS FOR DELETE BUTTON =================================
    async def delete_superusers(self, guild_id: int, values: list[str]) -> bool:
        user_ids_int = {int(user_id) for user_id in values}

        delete_scenario = self.db_factory.for_delete_set(
            guild_id=guild_id,
            values=user_ids_int,
            table_name='super_users',
            key='user_id'
        )

        result = await self.update_db_and_cache(
            scenario=delete_scenario,
            guild_id=guild_id
        )

        return result

    async def get_superusers_for_deletion(self, guild: discord.Guild, client: discord.Client) -> tuple:
        superusers = self.get_superusers(
            guild_id=guild.id
        )

        available_users: dict[int, str] = {}
        not_found_ids: set[int] = set()

        for user_id in superusers:
            member = guild.get_member(user_id)

            if member is not None:
                display = member.display_name
                global_name = member.global_name or member.name
                label = f'{display} ({global_name})'
                available_users[user_id] = label
            else:
                not_found_ids.add(user_id)

        if not_found_ids:
            result = await self.cleanup_service.cleanup_superusers(
                guild_id=guild.id,
                user_ids=not_found_ids
            )

            if not result:
                return (
                    available_users,
                    self._fetch_user_global_manes(
                        not_found_user_ids=not_found_ids,
                        client=client
                    ))

            not_found_usernames: list[str] = ['These users were not on this server and were deleted as well:',
                                              f'{'-' * 40}']

            for user_id in not_found_ids:
                user = await client.fetch_user(int(user_id))
                user_name = user.global_name or user.name
                not_found_usernames.append(f'🔸{user_name}')

            return available_users, '\n'.join(not_found_usernames)

        return available_users, False

    @staticmethod
    async def _fetch_user_global_manes(not_found_user_ids: set[int], client: discord.Client) -> str:
        not_found_names: list[str] = [
            'Some users were not found on this server, and were note deleted for some reason.'
            f' The names of users:', f'{'-' * 15}']

        for user_id in not_found_user_ids:
            user = await client.fetch_user(int(user_id))
            not_found_names.append(f'🔸{user.global_name}')

        return '\n'.join(not_found_names)

    def get_superusers(self, guild_id: int) -> set[int]:
        return self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=guild_id
        )
