from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.container import BotContainer
    from services.factories.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from services.buttons.navigator import Navigator

import discord

from core.container import AppContainer

from modules.buttons.for_admins.edit_settings_buttons.services.settings_formatter import SettingsFormatter

from database.settings_storage.settings_manager import StorageTarget

from services.embed_constructor.embed_constructor import (
    SuccessEmbed,
    ErrorEmbed
)


class HiddenRolesService:
    def __init__(self, navigator: Navigator):
        container: BotContainer = AppContainer.get()

        self.db_factory: DBFactory = container.db_factory
        self.settings: SettingsStorage = container.settings
        self.navigator = navigator
        self.formatter = SettingsFormatter()

    def for_add_roles_options(self, guild: discord.Guild):
        hidden_roles = self.settings.set_storage.for_set_get_all(
            target=StorageTarget.HIDDEN_ROLES,
            guild_id=guild.id
        )

        return [
            discord.SelectOption(
                label=role.name,
                value=str(role.id)
            )
            for role in guild.roles if role.id not in hidden_roles
        ]

    def for_remove_roles_options(self, guild: discord.Guild, target: StorageTarget):
        hidden_roles = self.settings.set_storage.for_set_get_all(
            target=target,
            guild_id=guild.id
        )
        available_items: dict[int, str] = {}
        for role_id in hidden_roles:
            role = guild.get_role(role_id)

            if not role:
                continue

            available_items[role_id] = role.name

        return [
            discord.SelectOption(
                label=v,
                value=str(k)
            )
            for k, v in sorted(available_items.items(), key=lambda i: i[0])
        ]

    async def for_add_role_save(self, interaction: discord.Interaction, value: list[str]):
        values = set(int(i) for i in value)
        self.settings.set_storage.for_set_add(
            target=StorageTarget.HIDDEN_ROLES,
            guild_id=interaction.guild_id,
            value=values
        )

        write = self.db_factory.for_write_set(
            guild_id=interaction.guild_id,
            values=values,
            table_name='roles',
            key='role_id'
        )

        db_result = await write.db_proceed()

        ch_names: list[str] = ['These roles have been successfully added to hidden']

        for role_id in values:
            role = interaction.guild.get_role(role_id)
            ch_names.append(f'🔸 {role.name}')

        result_msg = '\n'.join(ch_names)

        success_embed = SuccessEmbed(
            description=result_msg
        )

        error_embed = ErrorEmbed(
            description='Something went wrong, please try again later.'
        )

        settings_embed = await self.formatter.format_current_hidden_roles(interaction)

        await interaction.response.edit_message(
            embeds=[settings_embed, success_embed if db_result else error_embed]
        )

    async def for_remove_role_data(self, interaction: discord.Interaction, value: list[str]):
        values = set(int(i) for i in value)
        self.settings.set_storage.for_set_remove(
            target=StorageTarget.HIDDEN_ROLES,
            guild_id=interaction.guild_id,
            value=values
        )

        write = self.db_factory.for_delete_set(
            guild_id=interaction.guild_id,
            values=values,
            table_name='roles',
            key='role_id'
        )

        db_result = await write.db_proceed()

        ch_names: list[str] = ['These roles have been successfully deleted from hidden']

        for role_id in values:
            role = interaction.guild.get_role(role_id)
            ch_names.append(f'🔸 {role.name}')

        result_msg = '\n'.join(ch_names)

        success_embed = SuccessEmbed(
            description=result_msg
        )

        error_embed = ErrorEmbed(
            description='Something went wrong, please try again later.'
        )

        settings_embed = await self.formatter.format_current_hidden_roles(interaction)

        await interaction.response.edit_message(
            embeds=[settings_embed, success_embed if db_result else error_embed]
        )
