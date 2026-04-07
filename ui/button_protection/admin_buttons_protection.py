from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from ui.embed_constructor.embed_constructor import ErrorEmbed

if TYPE_CHECKING:
    from ui.button_protection.button_protection_service import ButtonProtectionService


class FirewallButton(discord.ui.Button):
    scope: str = "user"

    def __init__(
        self,
        protection_service: ButtonProtectionService,
        label: str,
        style: discord.ButtonStyle,
    ):
        super().__init__(label=label, style=style)

        self.protection_service = protection_service

    async def callback(self, interaction: discord.Interaction) -> None:
        if not self.protection_service.has_access(
            interaction=interaction, scope=self.scope
        ):
            error_embed = ErrorEmbed(description="⛔ You do not have permission.")
            await interaction.response.edit_message(embed=error_embed)
            return

        await self.on_click(interaction)

    async def on_click(self, interaction: discord.Interaction) -> None:
        raise NotImplementedError
