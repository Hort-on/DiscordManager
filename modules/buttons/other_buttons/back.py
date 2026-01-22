from __future__ import annotations

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.buttons.navigator import Navigator


class BackButton(FirewallButton):
    scope = 'user'

    def __init__(self, target: str, navigator: Navigator):
        super().__init__(
            label='↩️ Back',
            style=discord.ButtonStyle.secondary
        )
        self.target = target
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.navigator.go(target=self.target, interaction=interaction)
