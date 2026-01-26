from __future__ import annotations

import discord

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from services.buttons.navigator import Navigator


class BackButton(discord.ui.Button):
    def __init__(self, navigator: Navigator):
        super().__init__(
            label='↩️ Back',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def callback(self, interaction: discord.Interaction):
        context = getattr(self.view, 'context', None)

        if context is None:
            return

        prev = context.pop()
        if prev is None:
            return

        target, params = prev

        render = self.navigator.go(target, **params)

        if render.view is not None:
            render.view.context = context

        await interaction.response.edit_message(
            content=render.content,
            embed=render.embed,
            view=render.view
        )



