from __future__ import annotations

import discord

from core.container import AppContainer

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

from typing import TYPE_CHECKING

from services.embed_constructor.embed_constructor import InfoEmbed, WarningEmbed

if TYPE_CHECKING:
    from core.container import BotContainer


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
        lines: list[str] = ['Setting                  Status', '-----------------------  ----------']
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
            StorageTarget.SUPERUSERS,
            interaction.guild_id
        )

        if not users:
            lines.append('❌ not assigned')
        else:
            for user_id in users:
                member = interaction.guild.get_member(user_id)
                name = member.display_name if member else f'Unknown ({user_id})'
                lines.append(f'🔸 {name}')

        # ---- CHANNELS ----
        lines.append('')
        lines.append('Channels:')

        current_selected_channels = self.settings.dict_storage.for_dict_get_all(
            StorageTarget.SELECTED_CHANNELS,
            interaction.guild_id
        )

        if not current_selected_channels:
            lines.append('❌ NOT ASSIGNED')
        else:
            for key, value in current_selected_channels.items():
                channel = interaction.client.get_channel(value)
                channel_name = channel.name if channel else '❌ Not assigned'
                ch_label = key.replace('_channel_id', '')
                lines.append(f'🔸 {ch_label}: {channel_name}')

        description = '```text\n' + '\n'.join(lines) + '\n```'

        return InfoEmbed(description=description)
