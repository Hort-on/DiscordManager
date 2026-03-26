from __future__ import annotations

from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from general_services.translator.translator import Translator


class ReshuffleView(discord.ui.View):
    def __init__(self, *args, callback, translator: Translator, guild_id: int, **kwargs):
        super().__init__(timeout=None)
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.translator = translator

        @discord.ui.button(
            label=self.translator.t(
                guild_id=guild_id,
                section='RANDOMIZER',
                key='reshuffle'
            )
        )
        async def reshuffle(self, interaction: discord.Interaction, _):
            await self.callback(
                interaction,
                *self.args,
                edit_mode=True,
                **self.kwargs
            )

        self.add_item(reshuffle)
