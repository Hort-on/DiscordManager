from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator

import discord


class BackButton(discord.ui.Button):
    def __init__(self, navigator: Navigator):
        super().__init__(
            label='↩️ Back',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def callback(self, interaction: discord.Interaction):
        context = self.view.context
        if not context:
            print('Контекст не передано у BackButton')
            return

        prev = context.pop()
        if not prev:
            return

        target, params = prev

        view = self.navigator.go(
            route=target,
            params=params,
            context=context
        )

        view.context = context

        await interaction.response.edit_message(
            content=None,
            embeds=[],
            view=view
        )
