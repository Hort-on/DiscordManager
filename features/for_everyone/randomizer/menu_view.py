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


class RandomModeView(discord.ui.View):
    def __init__(self, navigator: Navigator, flow: RandomizerFlow):
        super().__init__(timeout=60)

        self.add_item(RandomNumButton(flow=flow))
        self.add_item(RandomWordButton(flow=flow))
        self.add_item(RandomTeamByText(flow=flow))
        self.add_item(RandomTeamByChannel(navigator=navigator, flow=flow))
        self.add_item(BackButton(navigator=navigator))
