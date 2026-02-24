from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from core.navigator import Navigator


async def _build_and_send_result(
        interaction: discord.Interaction,
        role_ids: set[int],
        text: str
) -> None:
    embed = None
    role_names: list[str] = [text]
    for role_id in role_ids:
        role = interaction.guild.get_role(role_id)
        role_names.append(f'🔸{role.name}')

        embed = SuccessEmbed(
            description='\n'.join(role_names)
        )

    await interaction.response.edit_message(embed=embed)


class AddRoleService:
    def __init__(
            self,
            navigator: Navigator,
            settings: SettingsStorage
    ):

        self.navigator = navigator
        self.settings = settings

    async def prepare_roles_for_addition(self, interaction: discord.Interaction):
        hidden_roles = self.settings.set_storage.for_set_get(
            target=StorageTarget.HIDDEN_ROLES,
            guild_id=interaction.guild_id
        )

        member_role_ids = {role.id for role in interaction.user.roles}
        guild_roles = interaction.guild.roles

        available_roles = {
            role.id: role.name
            for role in guild_roles
            if (
                    role.id not in hidden_roles
                    and role.id not in member_role_ids
                    and role.is_assignable()
            )
        }

        return [
            discord.SelectOption(
                label=name,
                value=str(role_id)
            )
            for role_id, name in sorted(
                available_roles.items(),
                key=lambda item: item[1].lower()
            )
        ]

    async def prepare_roles_for_deletion(self, interaction: discord.Interaction):
        hidden_roles = self.settings.set_storage.for_set_get(
            target=StorageTarget.HIDDEN_ROLES,
            guild_id=interaction.guild_id
        )

        member_roles = interaction.user.roles

        roles_to_remove = {
            role.id: role.name
            for role in member_roles
            if (
                role.id not in hidden_roles
                and role.is_assignable()
            )
        }

        return [
            discord.SelectOption(
                label=value,
                value=str(key)
            )
            for key, value in roles_to_remove.items()
        ]

    @staticmethod
    async def add_role_to_user(
            interaction: discord.Interaction,
            roles: list[str]
    ):
        member_role_ids = {role.id for role in interaction.user.roles}
        role_ids = {int(r_id) for r_id in roles}

        roles_to_add = []

        for role_id in role_ids:
            role = interaction.guild.get_role(role_id)
            if role and role_id not in member_role_ids:
                roles_to_add.append(role)

        if roles_to_add:
            await interaction.user.add_roles(*roles_to_add)

        await _build_and_send_result(
            interaction=interaction,
            role_ids=role_ids,
            text='The following roles have been successfully added:'
        )

    @staticmethod
    async def remove_role_from_user(
            interaction: discord.Interaction,
            roles: list[str]
    ):
        member_role_ids = {role.id for role in interaction.user.roles}
        role_ids = {int(r_id) for r_id in roles}

        roles_to_remove = []

        for role_id in role_ids:
            role = interaction.guild.get_role(role_id)
            if role and role.id in member_role_ids:
                roles_to_remove.append(role)

        if roles_to_remove:
            await interaction.user.remove_roles(*roles_to_remove)

        await _build_and_send_result(
            interaction=interaction,
            role_ids=role_ids,
            text='The following roles have been successfully removed:'
        )
