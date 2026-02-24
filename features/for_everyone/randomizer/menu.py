from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator_context import NavigationContext

if TYPE_CHECKING:
    from core.navigator import Navigator


class RandomMenuButton(discord.ui.Button):
    scope = 'user'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='🎲 Randomizer',
            style=discord.ButtonStyle.blurple
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        params_main = {
            'guild': interaction.guild,
            'user_id': interaction.user.id
        }

        context.push(target='main_menu', params=params_main)

        view = self.navigator.go(target='random_menu')

        view.context = context

        await interaction.response.edit_message(view=view)
