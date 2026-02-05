from __future__ import annotations

from typing import TYPE_CHECKING

from services.factories.db_factory.db_scenario_factory import DBFactory

if TYPE_CHECKING:
    from core.container import BotContainer
    from database.settings_storage.settings import SettingsStorage

import discord

from core.container import AppContainer

from database.settings_storage.settings_manager import StorageTarget

from services.embed_constructor.embed_constructor import (
    WarningEmbed,
    InfoEmbed
)


class CurrentSettings:
    def __init__(self):
        container: BotContainer = AppContainer.get()
        self.settings: SettingsStorage = container.settings
        self.db_factory: DBFactory = container.db_factory

    async def current_main_settings(self, interaction: discord.Interaction) -> discord.Embed:
        settings = self.settings.dict_storage.for_dict_get_all(
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id
        )

        if not settings:
            return WarningEmbed(description='No settings found.')
        lines: list[str] = [f'Setting {' ' * 18} Status', f'{'-' * 26}  {'-' * 15}']

        for key, value in sorted(settings.items(), key=lambda item: item[0]):
            if key == 'guild_id':
                continue
            status = '✅ Enabled' if value else '❌ Disabled'
            lines.append(f'🔸{key:<23}:  {status}')

        description = '```text\n' + '\n'.join(lines) + '\n```'

        return InfoEmbed(description=description)

    async def current_system_channels(self, interaction: discord.Interaction) -> discord.Embed:
        not_found_ch: set[int] = set()

        lines: list[str] = [f'System channels: {' ' * 18} Status', f'{'-' * 26}  {'-' * 15}', '']

        system_channels = self.settings.dict_storage.for_dict_get_all(
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=interaction.guild_id
        )

        if not system_channels:
            lines.append('❌ SYSTEM CHANNELS NOT FOUND')
        else:
            for key, value in system_channels.items():
                channel = interaction.client.get_channel(value)

                if not channel:
                    not_found_ch.add(value)
                    continue

                channel_name = channel.name if channel else '❌ Not assigned'
                ch_label = key.replace('_channel_id', '')
                lines.append(f'🔸 {ch_label}: {channel_name}')

        # if not_found_ch:
        #     await self._clean_up_not_founds(
        #         guild_id=interaction.guild_id,
        #         not_found_values=not_found_ch
        #     )

        description = '```text\n' + '\n'.join(lines) + '\n```'

        return InfoEmbed(description=description)

    async def current_hidden_channels(self, interaction: discord.Interaction) -> discord.Embed:
        not_found_ch: set[int] = set()

        lines: list[str] = [f'Hidden channels: {' ' * 18} Status', f'{'-' * 26}  {'-' * 15}', '']

        hidden_channels = self.settings.set_storage.for_set_get_all(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=interaction.guild_id
        )
        if not hidden_channels:
            lines.append('❌ HIDDEN CHANNELS NOT FOUND')
        else:
            for channel_id in hidden_channels:
                channel = interaction.client.get_channel(channel_id)

                if not channel:
                    not_found_ch.add(channel_id)
                    continue

                channel_name = channel.name if channel else '❌ Not assigned'
                lines.append(f'🔸 {channel_name}')

        # if not_found_ch:
        #     await self._clean_up_not_founds(
        #         guild_id=interaction.guild_id,
        #         not_found_values=not_found_ch
        #     )

        description = '```text\n' + '\n'.join(lines) + '\n```'

        return InfoEmbed(description=description)

    async def current_hidden_roles(self, interaction: discord.Interaction) -> discord.Embed:
        not_found_roles: set[int] = set()

        lines: list[str] = [f'Hidden roles:', f'{'-' * 13}', '']

        hidden_roles = self.settings.set_storage.for_set_get_all(
            target=StorageTarget.HIDDEN_ROLES,
            guild_id=interaction.guild_id
        )
        if not hidden_roles:
            lines.append('❌ HIDDEN ROLES NOT FOUND')
        else:
            for role_id in hidden_roles:
                role = interaction.guild.get_role(role_id)

                if not role:
                    not_found_roles.add(role_id)
                    continue

                channel_name = role.name if role else '❌ Not assigned'
                lines.append(f'🔸 {channel_name}')

        # if not_found_roles:
        #     await self._clean_up_not_founds(
        #         guild_id=interaction.guild_id,
        #         not_found_values=not_found_roles
        #     )

        description = '```text\n' + '\n'.join(lines) + '\n```'

        return InfoEmbed(description=description)

    # async def _clean_up_not_founds(self, guild_id: int, not_found_values: set[int]):


class SettingsFormatter:
    @staticmethod
    async def format_current_main_settings(interaction: discord.Interaction) -> discord.Embed:
        embed = await CurrentSettings().current_main_settings(interaction=interaction)
        return embed

    @staticmethod
    async def format_current_system_channels(interaction: discord.Interaction) -> discord.Embed:
        embed = await CurrentSettings().current_system_channels(interaction=interaction)
        return embed

    @staticmethod
    async def format_current_hidden_channels(interaction: discord.Interaction) -> discord.Embed:
        embed = await CurrentSettings().current_hidden_channels(interaction=interaction)
        return embed

    @staticmethod
    async def format_current_hidden_roles(interaction: discord.Interaction) -> discord.Embed:
        embed = await CurrentSettings().current_hidden_roles(interaction=interaction)
        return embed
