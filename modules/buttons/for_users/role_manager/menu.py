from __future__ import annotations

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.buttons.navigator import Navigator


class RoleManagerMenuButton(FirewallButton):
    scope = 'user'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Role manager',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        await self.navigator.go(
            target='role_manager_menu',
            interaction=interaction,
            ephemeral=True
        )
