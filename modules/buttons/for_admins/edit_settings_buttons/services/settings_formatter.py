from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.container import BotContainer
    from database.settings_storage.settings import SettingsStorage

import discord

import asyncio

from core.container import AppContainer

from database.settings_storage.settings_manager import StorageTarget

from services.embed_constructor.embed_constructor import WarningEmbed, InfoEmbed

from services.factories.db_factory.db_scenario_factory import DBFactory
from services.other_services.cleanup_service import CleanUpService


class CurrentSettings:
    def __init__(self):
        container: BotContainer = AppContainer.get()
        self.settings: SettingsStorage = container.settings
        self.db_factory: DBFactory = container.db_factory
        self.service = CleanUpService()

    def current_main_settings(self, interaction: discord.Interaction) -> discord.Embed:
        settings = self.settings.dict_storage.for_dict_get_all(
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id
        )

        if not settings:
            return WarningEmbed(description='No settings found.')
        lines: list[str] = [f'Setting{' ' * 14}Status', f'{'-' * 23}  {'-' * 12}']

        for key, value in sorted(settings.items(), key=lambda item: item[0]):
            if key == 'guild_id':
                continue

            if key == 'verification_role_id':
                role = interaction.guild.get_role(value)
                status = f'{role.name}' if value else '❌ Not assigned'
                lines.append(f'🔸{key:<20}: {status}')
                continue

            status = '✅ Enabled' if value else '❌ Disabled'
            lines.append(f'🔸{key:<20}: {status}')

        return InfoEmbed(description='```text\n' + '\n'.join(lines) + '\n```')

    def current_system_channels(self, guild: discord.Guild) -> list[discord.Embed]:
        not_found_ch: dict[str, int] = {}

        channels = self.settings.dict_storage.for_dict_get_all(
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild.id
        )

        lines: list[str] = [f'Current system channels{' ' * 3}channel names', f'{'-' * 23}{' ' * 3}{'-' * 15}']

        for k, v in sorted(channels.items(), key=lambda item: item[0]):
            ch = guild.get_channel(v)
            lines.append(f'{k:<23}: {ch.name if ch else '❗ not assigned'}')

        info_cleanup = None
        if not_found_ch:
            info_cleanup = asyncio.create_task(self.service.clean_up_system_channels(
                guild_id=guild.id,
                channels=channels
            ))

        info_embed = InfoEmbed(description='```text\n' + '\n'.join(lines) + '\n```')
        return [info_embed, info_cleanup if info_cleanup else None]

    def current_hidden_channels(self, interaction: discord.Interaction) -> list[discord.Embed]:
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

        info_cleanup = None
        if not_found_ch:
            info_cleanup = asyncio.create_task(self.service.clean_up_hidden_channels(
                guild_id=interaction.guild_id,
                values=not_found_ch
            ))

        description = '```text\n' + '\n'.join(lines) + '\n```'

        info_embed = InfoEmbed(description=description)

        return [info_embed, info_cleanup if info_cleanup else None]

    def current_hidden_roles(self, interaction: discord.Interaction) -> list[discord.Embed]:
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

        info_cleanup = None
        if not_found_roles:
            info_cleanup = asyncio.create_task(self.service.clean_up_hidden_roles(
                guild_id=interaction.guild_id,
                role_ids=not_found_roles
            ))

        description = '```text\n' + '\n'.join(lines) + '\n```'

        info_embed = InfoEmbed(description=description)

        return [info_embed, info_cleanup if info_cleanup else None]


class SettingsFormatter:
    @staticmethod
    def format_current_main_settings(interaction: discord.Interaction) -> discord.Embed:
        embed = CurrentSettings().current_main_settings(interaction=interaction)
        return embed

    @staticmethod
    def format_current_system_channels(guild: discord.Guild) -> list[discord.Embed]:
        embeds = CurrentSettings().current_system_channels(guild=guild)
        return embeds

    @staticmethod
    def format_current_hidden_channels(interaction: discord.Interaction) -> list[discord.Embed]:
        embeds = CurrentSettings().current_hidden_channels(interaction=interaction)
        return embeds

    @staticmethod
    def format_current_hidden_roles(interaction: discord.Interaction) -> list[discord.Embed]:
        embeds = CurrentSettings().current_hidden_roles(interaction=interaction)
        return embeds
