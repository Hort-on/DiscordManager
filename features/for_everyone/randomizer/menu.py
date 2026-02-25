from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.routes import Route
from core.navigator.navigator_context import NavigationContext

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator


class RandomMenuButton(discord.ui.Button):
    scope = 'user'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='🎲 Randomizer',
            style=discord.ButtonStyle.blurple
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        params_main = {
            'guild': interaction.guild,
            'user_id': interaction.user.id
        }

        view = self.navigator.random_menu()

        context = getattr(self.view, 'context', NavigationContext())

        context.push(target=Route.MAIN_MENU, params=params_main)

        view.context = context

        await interaction.response.edit_message(view=view)
