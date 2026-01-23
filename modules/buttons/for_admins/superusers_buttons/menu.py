from __future__ import annotations

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.buttons.for_admins.superusers_buttons.menu_view import SuperusersMenuView

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.buttons.navigator import Navigator


class SuperusersMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Superusers management',
            style=discord.ButtonStyle.green
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        view = SuperusersMenuView(navigator=self.navigator)
        await interaction.edit_original_response(view=view)
