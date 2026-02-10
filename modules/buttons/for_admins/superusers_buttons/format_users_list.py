from __future__ import annotations

from typing import TYPE_CHECKING

from database.settings_storage.settings_manager import StorageTarget
from services.embed_constructor.embed_constructor import InfoEmbed

if TYPE_CHECKING:
    from core.container import BotContainer
    from database.settings_storage.settings import SettingsStorage

import discord

from core.container import AppContainer


class SuperusersFormatter:
    def __init__(self):
        container: BotContainer = AppContainer.get()
        self.settings: SettingsStorage = container.settings

    def build_embed(self, interaction: discord.Interaction) -> discord.Embed:
        lines: list[str] = ['Current Superusers:', f'{'-' * 22}']

        users = self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=interaction.guild_id
        )

        if not users:
            return InfoEmbed(
                description='\n'.join(lines)
            )
        else:
            for user_id in users:
                member = interaction.guild.get_member(user_id)
                name = member.display_name if member else f'Unknown ({user_id})'
                lines.append(f'🔸 {name}')

            return InfoEmbed(
                description='\n'.join(lines)
            )
