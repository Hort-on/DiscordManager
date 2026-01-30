from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.container import BotContainer
    from database.settings_storage.settings import SettingsStorage

import discord

from core.container import AppContainer
from database.settings_storage.settings_manager import StorageTarget
from services.embed_constructor.embed_constructor import WarningEmbed, InfoEmbed


class EditSettingsResultScenario:
    def __init__(self):
        container: BotContainer = AppContainer.get()
        self.settings: SettingsStorage = container.settings

    async def build_result(self, interaction: discord.Interaction) -> discord.Embed:
        settings = self.settings.dict_storage.for_dict_get_all(
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id
        )

        if not settings:
            return WarningEmbed(description='No settings found.')
        lines: list[str] = [f'Setting {' ' * 18} Status', f'{'-' * 26}  {'-' * 15}']
        # ---- SETTINGS TABLE ----

        for key, value in settings.items():
            if key == 'guild_id':
                continue
            status = '✅ Enabled' if value else '❌ Disabled'
            lines.append(f'🔸{key:<23}:  {status}')

        # ---- SUPERUSERS ----
        lines.append('')
        lines.append('Superusers:')
        users = self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=interaction.guild_id
        )

        if not users:
            lines.append('❌ NOT ASSIGNED')
        else:
            for user_id in users:
                member = interaction.guild.get_member(user_id)
                name = member.display_name if member else f'Unknown ({user_id})'
                lines.append(f'🔸 {name}')

        # ---- ASSIGNED CHANNELS ----
        lines.append('')
        lines.append('Assigned channels:')

        assigned_channels = self.settings.dict_storage.for_dict_get_all(
            target=StorageTarget.SELECTED_CHANNELS,
            guild_id=interaction.guild_id
        )

        if not assigned_channels:
            lines.append('❌ NOT ASSIGNED')
        else:
            for key, value in assigned_channels.items():
                channel = interaction.client.get_channel(value)
                channel_name = channel.name if channel else '❌ Not assigned'
                ch_label = key.replace('_channel_id', '')
                lines.append(f'🔸 {ch_label}: {channel_name}')

        # ---- HIDDEN CHANNELS ----
        lines.append('')
        lines.append('Hidden channels:')

        hidden_channels = self.settings.set_storage.for_set_get_all(
            target=StorageTarget.SELECTED_CHANNELS,
            guild_id=interaction.guild_id
        )
        if not hidden_channels:
            lines.append('❌ NOT ASSIGNED')
        else:
            for channel_id in hidden_channels:
                channel = interaction.client.get_channel(channel_id)
                channel_name = channel.name if channel else '❌ Not assigned'
                lines.append(f'🔸 {channel_name}')

        description = '```text\n' + '\n'.join(lines) + '\n```'

        return InfoEmbed(description=description)


class SettingsFormatter:
    @staticmethod
    async def format_settings(interaction: discord.Interaction) -> discord.Embed:
        embed = await EditSettingsResultScenario().build_result(interaction=interaction)
        return embed
