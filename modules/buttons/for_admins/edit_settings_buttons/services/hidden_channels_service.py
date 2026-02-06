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


class HiddenChannelsService:
    def __init__(self, navigator: Navigator):
        container: BotContainer = AppContainer.get()

        self.db_factory: DBFactory = container.db_factory
        self.settings: SettingsStorage = container.settings
        self.navigator = navigator

    def for_add_channel_options(self, guild: discord.Guild):
        result = self.settings.set_storage.for_set_get_all(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=guild.id
        )

        return [
            discord.SelectOption(
                label=channel.name,
                value=str(channel.id)
            )
            for channel in guild.channels if channel.id not in result
        ]

    def for_remove_channel_options(self, guild: discord.Guild):
        hidden_channels = self.settings.set_storage.for_set_get_all(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=guild.id
        )
        available_items: dict[int, str] = {}
        for channel_id in hidden_channels:
            channel = guild.get_channel(channel_id)

            if not channel:
                continue

            available_items[channel_id] = channel.name

        return [
            discord.SelectOption(
                label=v,
                value=str(k)
            )
            for k, v in sorted(available_items.items(), key=lambda i: i[0])
        ]

    async def for_add_channel_save(self, interaction: discord.Interaction, value: list[str]):
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
        settings_embeds = formatter.format_current_hidden_channels(interaction)

        await interaction.response.edit_message(
            embeds=[settings_embeds[0], settings_embeds[1], success_embed if db_result else error_embed]
        )

    async def for_remove_channel_data(self, interaction: discord.Interaction, value: list[str]):
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
        settings_embeds = formatter.format_current_hidden_channels(interaction)

        await interaction.response.edit_message(
            embeds=[settings_embeds[0], settings_embeds[1], success_embed if db_result else error_embed]
        )
