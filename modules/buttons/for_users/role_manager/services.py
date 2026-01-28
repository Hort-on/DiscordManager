from __future__ import annotations

import discord

from core.container import AppContainer

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

from services.drop_down_menu.drop_down_selector import DropMenuView
from services.embed_constructor.embed_constructor import SuccessEmbed

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.container import BotContainer


async def _build_and_send_result(
        interaction: discord.Interaction,
        role_ids: set[int],
        text: str
) -> None:
    role_names: list[str] = [text]
    for role_id in role_ids:
        role = interaction.guild.get_role(role_id)
        role_names.append(role.name)

        embed = SuccessEmbed(
            description='\n' + '-> '.join(role_names)
        )

        await interaction.response.edit_message(embed=embed)


class AddRoleService:
    def __init__(self):
        container: BotContainer = AppContainer.get()

        self.settings: SettingsStorage = container.settings

    async def prepare_roles(self, interaction: discord.Interaction):
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

        options = [
            discord.SelectOption(
                label=name,
                value=str(role_id)
            )
            for role_id, name in sorted(
                available_roles.items(),
                key=lambda item: item[1].lower()
            )
        ]

        view = DropMenuView(
            options=options,
            placeholder='Here are roles I can add to you:',
            callback=self._add_role_to_user,
            max_values=25
        )

        await interaction.response.edit_message(
            content='Please choose the roles you want to add:',
            view=view
        )

    @staticmethod
    async def _add_role_to_user(
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


class RemoveRoleService:
    def __init__(self):
        container: BotContainer = AppContainer.get()

        self.settings: SettingsStorage = container.settings

    async def prepare_roles(self, interaction: discord.Interaction):
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

        options = [
            discord.SelectOption(
                label=value,
                value=str(key)
            )
            for key, value in roles_to_remove.items()
        ]

        view = DropMenuView(
            options=options,
            placeholder='Here are the roles I can remove from you:',
            callback=self._remove_role_from_user,
            max_values=25
        )

        await interaction.response.edit_message(
            content='Please choose the roles you want to remove:',
            view=view
        )

    @staticmethod
    async def _remove_role_from_user(
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
