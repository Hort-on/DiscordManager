from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage


@dataclass
class AddedRolesResult:
    added_roles: set[discord.Role]
    not_added_roles: set[discord.Role] | None = None


@dataclass
class RemoveRolesResult:
    removed_roles: set[discord.Role]
    not_removed_roles: set[discord.Role] | None = None


class RoleManagerService:
    def __init__(self, settings: SettingsStorage):
        self.settings = settings

    @staticmethod
    async def add_roles_to_user(member: discord.Member, guild: discord.Guild, roles: list[str]) -> AddedRolesResult:
        role_ids = {int(r_id) for r_id in roles}

        roles_to_add: set[discord.Role] = set()

        for role_id in role_ids:
            role = guild.get_role(role_id)
            if role and role not in member.roles:
                roles_to_add.add(role)

        try:
            await member.add_roles(*roles_to_add)
        except discord.Forbidden:
            added_roles: set[discord.Role] = set()
            not_added_roles: set[discord.Role] = set()

            for role in roles_to_add:
                try:
                    await member.add_roles(role)
                    added_roles.add(role)
                except discord.Forbidden:
                    not_added_roles.add(role)

            return AddedRolesResult(
                added_roles=added_roles,
                not_added_roles=not_added_roles
            )

        return AddedRolesResult(
            added_roles=roles_to_add
        )

    @staticmethod
    async def remove_roles_from_user(
            guild: discord.Guild,
            member: discord.Member,
            roles: list[str]
    ) -> RemoveRolesResult:
        role_ids = {int(r_id) for r_id in roles}

        roles_to_remove: set[discord.Role] = set()

        for role_id in role_ids:
            role = guild.get_role(role_id)
            if role in member.roles:
                roles_to_remove.add(role)

        try:
            await member.remove_roles(*roles_to_remove)
        except discord.Forbidden:
            removed_roles: set[discord.Role] = set()
            not_removed_roles: set[discord.Role] = set()

            for role in roles_to_remove:
                try:
                    await member.remove_roles(role)
                    removed_roles.add(role)
                except discord.Forbidden:
                    not_removed_roles.add(role)

            return RemoveRolesResult(
                removed_roles=removed_roles,
                not_removed_roles=not_removed_roles
            )

        return RemoveRolesResult(
            removed_roles=roles_to_remove
        )

    def get_hidden_roles(self, guild_id: int) -> set[int]:
        return self.settings.set_storage.for_set_get(
            target=StorageTarget.HIDDEN_ROLES,
            guild_id=guild_id
        )
