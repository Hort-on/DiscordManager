from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from general_services.other_services.cleanup_service import CleanUpService

import discord

from database.settings_storage.settings_manager import StorageTarget

from ui.embed_constructor.embed_constructor import WarningEmbed, InfoEmbed


class CurrentSettings:
    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBFactory,
            cleanup_service: CleanUpService
    ):
        self.settings = settings
        self.db_factory = db_factory
        self.service = cleanup_service

    def current_main_settings(self, interaction: discord.Interaction) -> discord.Embed:
        settings = self.settings.dict_storage.for_dict_get(
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

    async def current_system_channels(self, guild: discord.Guild) -> discord.Embed:
        not_found_ch: list[str] = []

        channels = self.settings.dict_storage.for_dict_get(
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild.id
        )

        lines: list[str] = [f'System channels{' ' * 8}channel names',
                            f'{'-' * 21}{' ' * 2}{'-' * 14}']

        for key, value in sorted(channels.items(), key=lambda item: item[0]):
            channel = guild.get_channel(value)

            if not channel and value is not None:
                not_found_ch.append(key)

            config_name = key.removesuffix('_id').replace('_', ' ')
            lines.append(f'{config_name:<20}: {channel.name if channel else '❗ not assigned'}')

        if not_found_ch:
            msg = await self.service.clean_up_system_channels(
                guild_id=guild.id,
                channels=not_found_ch
            )
            lines.append(f'\n\n{msg}')

        info_embed = InfoEmbed(description='```text\n' + '\n'.join(lines) + '\n```')

        return info_embed

    async def current_hidden_channels(self, interaction: discord.Interaction) -> discord.Embed:
        not_found_ch: set[int] = set()

        lines: list[str] = [f'Hidden channels:', f'{'-' * 16}']

        hidden_channels = self.settings.set_storage.for_set_get(
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

        if not_found_ch:
            msg = await self.service.clean_up_hidden_channels(
                guild_id=interaction.guild_id,
                values=not_found_ch
            )
            lines.append(f'\n\n{msg}')

        description = '```text\n' + '\n'.join(lines) + '\n```'

        info_embed = InfoEmbed(description=description)

        return info_embed

    async def current_hidden_roles(self, interaction: discord.Interaction) -> discord.Embed:
        not_found_roles: set[int] = set()

        lines: list[str] = [f'Hidden roles:', f'{'-' * 13}']

        hidden_roles = self.settings.set_storage.for_set_get(
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

        if not_found_roles:
            msg = await self.service.clean_up_hidden_roles(
                guild_id=interaction.guild_id,
                role_ids=not_found_roles
            )
            lines.append(f'\n\n{msg}')

        description = '```text\n' + '\n'.join(lines) + '\n```'

        info_embed = InfoEmbed(description=description)

        return info_embed


class SettingsFormatter:
    @staticmethod
    def format_current_main_settings(interaction: discord.Interaction) -> discord.Embed:
        embed = CurrentSettings().current_main_settings(interaction=interaction)
        return embed

    @staticmethod
    async def format_current_system_channels(guild: discord.Guild) -> discord.Embed:
        embed = await CurrentSettings().current_system_channels(guild=guild)
        return embed

    @staticmethod
    async def format_current_hidden_channels(interaction: discord.Interaction) -> discord.Embed:
        embed = await CurrentSettings().current_hidden_channels(interaction=interaction)
        return embed

    @staticmethod
    async def format_current_hidden_roles(interaction: discord.Interaction) -> discord.Embed:
        embed = await CurrentSettings().current_hidden_roles(interaction=interaction)
        return embed
