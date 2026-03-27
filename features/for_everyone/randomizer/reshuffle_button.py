from __future__ import annotations

from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from general_services.translator.translator import Translator


class ReshuffleView(discord.ui.View):
    def __init__(self, *args, callback, translator: Translator, guild_id: int, **kwargs):
        super().__init__(timeout=None)

        @discord.ui.button(
            label=translator.t(
                guild_id=guild_id,
                section='RANDOMIZER',
                key='reshuffle'
            )
        )
        async def reshuffle(interaction: discord.Interaction, _):
            await callback(
                interaction,
                *args,
                edit_mode=True,
                **kwargs
            )

        self.add_item(reshuffle)
