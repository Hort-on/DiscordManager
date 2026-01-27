from __future__ import annotations

import discord

from core.container import AppContainer

from modules.buttons.button_protection.protector import ButtonPermissionService

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.container import BotContainer


class FirewallButton(discord.ui.Button):
    scope: str = 'user'
    use_modal = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container: BotContainer = AppContainer.get()

    async def callback(self, interaction: discord.Interaction):
        button_permission = ButtonPermissionService(self.container.settings)
        if not self.use_modal:
            if not interaction.response.is_done():
                await interaction.response.defer(ephemeral=True)

        if not button_permission.has_access(
                interaction=interaction,
                scope=self.scope
        ):
            await interaction.edit_original_response(
                content='⛔ You do not have permission'
            )
            return

        await self.on_click(interaction)

    async def on_click(self, interaction):
        raise NotImplementedError
