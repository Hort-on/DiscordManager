from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from general_services.other_services.cleanup_service import CleanUpService

import discord

from database.settings_storage.settings_manager import StorageTarget

from ui.embed_constructor.embed_constructor import InfoEmbed


class SettingsFormatter:
    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBFactory,
            cleanup_service: CleanUpService
    ):
        self.settings = settings
        self.db_factory = db_factory
        self.service = cleanup_service

    def format_current_main_settings(self, interaction: discord.Interaction) -> discord.Embed:
        settings = self.settings.dict_storage.get_all(
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id
        )

        lines: list[str] = [f'Setting{" " * 14}Status', f'{"-" * 23}  {"-" * 12}']

        for key, value in sorted(settings.items()):
            if key == 'guild_id':
                continue

            config_name = key.removesuffix('_id').replace('_', ' ')
            status = self._format_status(interaction=interaction, key=key, value=value)
            lines.append(f'🔸{config_name:<20}: {status}')

        return InfoEmbed(description='```text\n' + '\n'.join(lines) + '\n```')

    @staticmethod
    def _format_status(interaction: discord.Interaction, key: str, value) -> str:
        if key == 'verification_role_id':
            role = interaction.guild.get_role(value)
            return role.name if value else '❌ not assigned'

        if key == 'verification_message_id':
            return '✅ assigned' if value else '❌ not assigned'

        if key == 'language':
            return 'ukrainian' if value == 'uk' else 'english'

        return '✅ Enabled' if value else '❌ Disabled'

    async def format_current_system_channels(self, guild: discord.Guild) -> discord.Embed:
        not_found_ch: list[str] = []

        channels = self.settings.dict_storage.get_all(
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

    async def format_current_hidden(
            self,
            interaction: discord.Interaction,
            target: StorageTarget,
    ) -> discord.Embed:
        is_channel = target == StorageTarget.HIDDEN_CHANNELS

        guild = interaction.guild

        title = 'Hidden channels:' if is_channel else 'Hidden roles:'
        not_found_label = '❌ HIDDEN CHANNELS NOT FOUND' if is_channel else '❌ HIDDEN ROLES NOT FOUND'

        lines: list[str] = [title, '-' * 16]
        not_found: set[int] = set()

        items = self.settings.set_storage.for_set_get(
            target=target,
            guild_id=guild.id
        )

        if not items:
            lines.append(not_found_label)
        else:
            for item_id in items:
                item = (
                    guild.get_channel(item_id)
                    if is_channel else
                    guild.get_role(item_id)
                )

                if not item:
                    not_found.add(item_id)
                    continue

                lines.append(f'🔸 {item.name}')

        if not_found:
            message = await (
                self.service.clean_up_hidden_channels(guild_id=guild.id, values=not_found)
                if is_channel else
                self.service.clean_up_hidden_roles(guild_id=guild.id, role_ids=not_found)
            )
            lines.append(f'\n\n{message}')

        return InfoEmbed(description='```text\n' + '\n'.join(lines) + '\n```')
