from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.container import BotContainer

import discord

from core.container import AppContainer

from modules.buttons.button_protection.protector import ButtonPermissionService

from ui.embed_constructor.embed_constructor import ErrorEmbed


class FirewallButton(discord.ui.Button):
    scope: str = 'user'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container: BotContainer = AppContainer.get()

    async def callback(self, interaction: discord.Interaction):
        permission = ButtonPermissionService(self.container.settings)

        if not permission.has_access(
            interaction=interaction,
            scope=self.scope
        ):
            error_embed = ErrorEmbed(
                description='⛔ You do not have permission.'
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        await self.on_click(interaction)

    async def on_click(self, interaction: discord.Interaction):
        raise NotImplementedError
