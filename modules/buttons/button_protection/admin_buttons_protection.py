from typing import TYPE_CHECKING

import discord

from core.container import AppContainer

from modules.buttons.button_protection.protector import ButtonPermissionService

if TYPE_CHECKING:
    from core.controller import BotController


class FirewallButton(discord.ui.Button):
    scope: str = 'user'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        controller: 'BotController' = AppContainer.get()
        self.button_permission = ButtonPermissionService(controller.settings)

    async def callback(self, interaction: discord.Interaction):
        if not self.button_permission.has_access(
            interaction=interaction,
            scope=self.scope
        ):
            return await interaction.edit_original_response(
                content='⛔ You do not have permission to use this functionality!'
            )

        await self.on_click(interaction)

    async def on_click(self, interaction: discord.Interaction) -> None:
        raise NotImplementedError
