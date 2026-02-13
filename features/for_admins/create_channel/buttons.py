from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.navigator import Navigator

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton


class CreateChannelButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Create a channel',
            style=discord.ButtonStyle.blurple
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        ...
