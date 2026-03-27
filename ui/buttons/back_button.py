from __future__ import annotations

from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from general_services.translator.translator import Translator


class BackButton(discord.ui.Button):
    def __init__(self, navigator: Navigator, translator: Translator, guild_id: int):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='SYSTEM_GENERAL',
                key='back_button'
            ),
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def callback(self, interaction: discord.Interaction):
        context = self.view.context
        if not context:
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
