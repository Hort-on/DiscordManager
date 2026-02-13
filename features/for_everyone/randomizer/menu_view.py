from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.navigator import Navigator

import discord

from modules.buttons.for_users.randomizer.buttons import (
    RandomNumButton,
    RandomWordButton,
    RandomTeamByMsg,
    RandomTeamByChannel
)

from modules.buttons.other_buttons.back import BackButton


class RandomModeView(discord.ui.View):
    def __init__(self, navigator: Navigator):
        super().__init__(timeout=60)

        self.add_item(RandomNumButton())
        self.add_item(RandomWordButton())
        self.add_item(RandomTeamByMsg())
        self.add_item(RandomTeamByChannel(navigator=navigator))
        self.add_item(BackButton(navigator=navigator))

