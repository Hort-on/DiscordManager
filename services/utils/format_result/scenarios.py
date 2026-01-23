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
        controller: BotContainer = AppContainer.get()

        self.settings: SettingsStorage = controller.settings

    async def build_result(self, interaction: discord.Interaction) -> discord.Embed:
        lines: list[str] = ['Your current settings:\n']

        settings = self.settings.dict_storage.for_dict_get_all(
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id
        )

        if not settings:
            embed = WarningEmbed(
                description='No settings found.'
            )
            return embed

        for key, value in settings.items():
            status = '✅ Enabled' if value else '❌ Disabled'
            lines.append(f'-> {key}: {status}')

        result = self._append_superusers(interaction, lines)

        return result

    def _append_superusers(self, interaction, lines) -> discord.Embed | None:
        users = self.settings.set_storage.for_set_get(
            StorageTarget.SUPERUSERS,
            interaction.guild_id
        )

        lines.append('\nSuperusers:')

        if not users:
            lines.append('-> not assigned')

            result = self._append_channels(interaction=interaction, lines=lines)
            return result

        for user_id in users:
            member = interaction.guild.get_member(user_id)
            name = member.display_name if member else f'Unknown ({user_id})'
            lines.append(f'-> {name}')

        result = self._append_channels(interaction=interaction, lines=lines)
        return result

    def _append_channels(self, interaction: discord.Interaction, lines) -> discord.Embed:
        current_selected_channels = self.settings.dict_storage.for_dict_get_all(
            StorageTarget.SELECTED_CHANNELS,
            interaction.guild_id
        )

        lines.append('\n Channels:')

        for key, value in current_selected_channels.items():
            channel = interaction.client.get_channel(value)
            status = channel.name if channel is not None else '❌ Not assigned'
            ch_name = key.replace('_channel_id', ' channel')
            lines.append(f'-> {ch_name}: {status}')

        final_result = '\n' + '-> '.join(lines)

        embed = InfoEmbed(
            description=final_result
        )

        return embed
