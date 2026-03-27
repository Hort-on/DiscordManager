from __future__ import annotations

from typing import TYPE_CHECKING
import discord

from features.for_everyone.randomizer.buttons import (
    RandomNumButton,
    RandomWordButton,
    RandomTeamByText,
    RandomTeamByChannel
)

from ui.buttons.back_button import BackButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_everyone.randomizer.flow import RandomizerFlow
    from general_services.translator.translator import Translator


class RandomModeView(discord.ui.View):
    def __init__(self, navigator: Navigator, flow: RandomizerFlow, translator: Translator, guild_id: int):
        super().__init__(timeout=60)

        self.add_item(
            RandomNumButton(
                flow=flow,
                translator=translator,
                guild_id=guild_id
            )
        )
        self.add_item(
            RandomWordButton(
                flow=flow,
                translator=translator,
                guild_id=guild_id
            )
        )
        self.add_item(
            RandomTeamByText(
                flow=flow,
                translator=translator,
                guild_id=guild_id
            )
        )
        self.add_item(
            RandomTeamByChannel(
                navigator=navigator,
                flow=flow,
                translator=translator,
                guild_id=guild_id
            )
        )
        self.add_item(
            BackButton(
                navigator=navigator,
                translator=translator,
                guild_id=guild_id
            )
        )
