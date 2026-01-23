from __future__ import annotations

import discord

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.buttons.navigator import Navigator


class BackButton(discord.ui.Button):
    def __init__(self, target: str, navigator: Navigator):
        super().__init__(
            label='↩️ Back',
            style=discord.ButtonStyle.secondary
        )
        self.target = target
        self.navigator = navigator

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        await self.navigator.go(target=self.target, interaction=interaction)
