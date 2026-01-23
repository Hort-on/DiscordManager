from __future__ import annotations

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.buttons.navigator import Navigator


class AdminMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Admin menu',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator
        print('адмін меню')

    async def on_click(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        print('початок callback')
        await self.navigator.go(
            target='admin_menu',
            interaction=interaction,
            ephemeral=True
        )
        print('кінець Callback')
