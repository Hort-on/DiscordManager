from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings_manager import StorageTarget

from ui.embed_constructor.embed_constructor import InfoEmbed

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage


class SuperusersFormatter:
    def __init__(self, settings: SettingsStorage):
        self.settings = settings

    def build_embed(self, guild: discord.Guild) -> discord.Embed:
        lines: list[str] = ['Current Superusers:', f'{'-' * 22}']

        users = self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=guild.id
        )

        if not users:
            return InfoEmbed(
                description='\n'.join(lines)
            )
        else:
            for user_id in users:
                member = guild.get_member(user_id)
                name = member.display_name if member else f'Unknown ({user_id})'
                lines.append(f'🔸 {name}')

            return InfoEmbed(
                description='\n'.join(lines)
            )
