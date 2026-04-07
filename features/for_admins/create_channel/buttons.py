from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from ui.button_protection.button_protection_service import ButtonProtectionService


class CreateChannelButton(FirewallButton):
    scope = "admin"

    def __init__(self, service: ButtonProtectionService):
        super().__init__(
            label="Create a channel",
            style=discord.ButtonStyle.blurple,
            protection_service=service,
        )

    async def on_click(self, interaction: discord.Interaction) -> None: ...
