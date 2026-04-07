from __future__ import annotations

from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from general_services.translator.translator import Translator


class ReshuffleButton(discord.ui.Button):
    def __init__(
        self, *args, callback, translator: Translator, guild_id: int, **kwargs
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id, section="RANDOMIZER", key="reshuffle"
            ),
            style=discord.ButtonStyle.primary,
        )
        self.callback_func = callback
        self.args = args
        self.kwargs = kwargs

    async def callback(self, interaction: discord.Interaction):
        await self.callback_func(interaction, *self.args, edit_mode=True, **self.kwargs)


class ReshuffleView(discord.ui.View):
    def __init__(
        self, *args, callback, translator: Translator, guild_id: int, **kwargs
    ):
        super().__init__(timeout=None)

        self.add_item(
            ReshuffleButton(
                *args,
                callback=callback,
                translator=translator,
                guild_id=guild_id,
                **kwargs,
            )
        )
