from __future__ import annotations

import discord

from core.container import AppContainer

from modules.buttons.button_protection.protector import ButtonPermissionService

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.container import BotContainer


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
            await interaction.response.edit_message(
                content='⛔ You do not have permission',
                view=None
            )
            return

        await self.on_click(interaction)

    async def on_click(self, interaction: discord.Interaction):
        raise NotImplementedError

