from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.container import BotContainer
    from services.factories.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from services.buttons.navigator import Navigator

import discord

import asyncio

from core.container import AppContainer

from database.settings_storage.settings_manager import StorageTarget

from modules.buttons.for_admins.edit_settings_buttons.settings_formatter import SettingsFormatter

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

    def for_add_build_options(self, guild: discord.Guild):
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

    async def for_add_save_data(self, interaction: discord.Interaction, value: list[str]):
        values = set(int(i) for i in value)
        self.settings.set_storage.for_set_add(
            target=StorageTarget.HIDDEN_ROLES,
            guild_id=interaction.guild_id,
            value=values
        )

        write = self.db_factory.for_write_set(
            guild_id=interaction.guild_id,
            values=values,
            table_name='roles'
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

    def for_delete_build_options(self, guild: discord.Guild):
        not_found: set[int] = set()

        hidden_ch = self.settings.set_storage.for_set_get_all(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=guild.id
        )
        print(hidden_ch)

        channels: dict[int, str] = {}
        for ch_id in hidden_ch:
            channel = guild.get_channel(ch_id)

            if not channel:
                not_found.add(ch_id)
                continue

            channels[ch_id] = channel.name

        if not_found:
            asyncio.create_task(self._cleanup(guild_id=guild.id, values=not_found))

        print(channels)

        return [
            discord.SelectOption(
                label=v,
                value=str(k)
            )
            for k, v in sorted(channels.items(), key=lambda i: i[0])
        ]

    async def for_delete_save_data(self, interaction: discord.Interaction, value: list[str]):
        values = set(int(i) for i in value)
        self.settings.set_storage.for_set_remove(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=interaction.guild_id,
            value=values
        )

        write = self.db_factory.for_delete_set(
            guild_id=interaction.guild_id,
            values=values,
            table_name='roles'
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

    async def _cleanup(self, guild_id: int, values: set[int]):
        self.settings.set_storage.for_set_remove(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=guild_id,
            value=values
        )

        write = self.db_factory.for_delete_set(
            guild_id=guild_id,
            values=values,
            table_name='roles'
        )

        await write.db_proceed()
