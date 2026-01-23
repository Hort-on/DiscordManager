from __future__ import annotations

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.buttons.navigator import Navigator


class EditSettingsButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Edit settings',
            style=discord.ButtonStyle.green
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.navigator.go(
            target='edit_settings',
            interaction=interaction
        )
