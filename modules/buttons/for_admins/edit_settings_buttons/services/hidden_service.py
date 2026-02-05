from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.container import BotContainer
    from services.factories.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from services.buttons.navigator import Navigator

import discord

from core.container import AppContainer

from modules.buttons.for_admins.edit_settings_buttons.settings_formatter import SettingsFormatter

from database.settings_storage.settings_manager import StorageTarget

from services.embed_constructor.embed_constructor import (
    SuccessEmbed,
    ErrorEmbed
)


class HiddenService:
    def __init__(self, navigator: Navigator):
        container: BotContainer = AppContainer.get()

        self.db_factory: DBFactory = container.db_factory
        self.settings: SettingsStorage = container.settings
        self.navigator = navigator

    def for_add_build_options(self, guild_id: int, target: StorageTarget, storage):
        result = self.settings.set_storage.for_set_get_all(
            target=target,
            guild_id=guild_id
        )

        return [
            discord.SelectOption(
                label=item.name,
                value=str(item.id)
            )
            for item in storage if item.id not in result
        ]

    def for_delete_build_options(self, guild: discord.Guild, target: StorageTarget):
        items = self.settings.set_storage.for_set_get_all(
            target=target,
            guild_id=guild.id
        )
        available_items: dict[int, str] = {}
        for item_id in items:
            if target == StorageTarget.HIDDEN_CHANNELS:
                item = guild.get_channel(item_id)
            else:
                item = guild.get_role(item_id)

            if not item:
                continue

            available_items[item_id] = item.name

        return [
            discord.SelectOption(
                label=v,
                value=str(k)
            )
            for k, v in sorted(available_items.items(), key=lambda i: i[0])
        ]

    async def for_add_ch_save(self, interaction: discord.Interaction, value: list[str]):
        values = set(int(i) for i in value)
        self.settings.set_storage.for_set_add(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=interaction.guild_id,
            value=values
        )

        write = self.db_factory.for_write_set(
            guild_id=interaction.guild_id,
            values=values,
            table_name='hidden_channels',
            key='channel_id'
        )

        db_result = await write.db_proceed()

        ch_names: list[str] = ['These channels have been successfully added to hidden']

        for ch_id in values:
            channel = interaction.guild.get_channel(ch_id)
            ch_names.append(f'🔸 {channel.name}')

        result_msg = '\n'.join(ch_names)

        success_embed = SuccessEmbed(
            description=result_msg
        )

        error_embed = ErrorEmbed(
            description='Something went wrong, please try again later.'
        )

        formatter = SettingsFormatter()
        settings_embed = await formatter.format_current_hidden_channels(interaction)

        await interaction.response.edit_message(
            embeds=[settings_embed, success_embed if db_result else error_embed]
        )

    async def for_remove_ch_data(self, interaction: discord.Interaction, value: list[str]):
        values = set(int(i) for i in value)
        self.settings.set_storage.for_set_remove(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=interaction.guild_id,
            value=values
        )

        write = self.db_factory.for_delete_set(
            guild_id=interaction.guild_id,
            values=values,
            table_name='hidden_channels',
            key='channel_id'
        )

        db_result = await write.db_proceed()

        ch_names: list[str] = ['These channels have been successfully deleted from hidden']

        for ch_id in values:
            channel = interaction.guild.get_channel(ch_id)
            ch_names.append(f'🔸 {channel.name}')

        result_msg = '\n'.join(ch_names)

        success_embed = SuccessEmbed(
            description=result_msg
        )

        error_embed = ErrorEmbed(
            description='Something went wrong, please try again later.'
        )

        formatter = SettingsFormatter()
        settings_embed = await formatter.format_current_hidden_channels(interaction)

        await interaction.response.edit_message(
            embeds=[settings_embed, success_embed if db_result else error_embed]
        )

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

        formatter = SettingsFormatter()
        settings_embed = await formatter.format_current_hidden_roles(interaction)

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

        formatter = SettingsFormatter()
        settings_embed = await formatter.format_current_hidden_roles(interaction)

        await interaction.response.edit_message(
            embeds=[settings_embed, success_embed if db_result else error_embed]
        )
