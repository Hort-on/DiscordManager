from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.for_everyone.birthdays.buttons import AddBirthdayButton, DeleteBirthdayButton

from ui.buttons.back_button import BackButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_everyone.birthdays.flow import BirthdayFlow


class BirthdayMenuView(discord.ui.View):
    def __init__(self, navigator: Navigator, flow: BirthdayFlow):
        super().__init__(timeout=60)

        self.add_item(AddBirthdayButton(
            flow=flow
        ))
        self.add_item(DeleteBirthdayButton(
            flow=flow
        ))
        self.add_item(BackButton(navigator=navigator))
