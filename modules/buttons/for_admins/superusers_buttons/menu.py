from __future__ import annotations

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton

from typing import TYPE_CHECKING

from services.buttons.navigator_context import NavigationContext

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator


class SuperusersMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Superusers management',
            style=discord.ButtonStyle.green
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = NavigationContext()

        context.back_view(target='admin_menu', params={'guild_id': interaction.guild_id})

        view = self.navigator.go(target='superusers_menu')

        view.context = context

        await interaction.response.edit_message(view=view)
