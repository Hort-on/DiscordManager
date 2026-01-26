from __future__ import annotations

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton

from services.buttons.navigator_context import NavigationContext

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from services.buttons.navigator import Navigator


class AdminMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Admin menu',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction):
        context = NavigationContext()

        params = {
            'guild_id': interaction.guild_id
        }

        context.push(target='main_menu', params=params)

        render = self.navigator.go(target='admin_menu', **params)

        render.view.context = context

        await interaction.response.edit_message(
            view=render.view
        )
