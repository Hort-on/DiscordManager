from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator

import discord

from modules.buttons.for_admins.birthday_buttons.buttons import AddBirthdayButton, DeleteBirthdayButton
from modules.buttons.other_buttons.back import BackButton


class BirthdayMenuView(discord.ui.View):
    def __init__(self, navigator: Navigator):
        super().__init__(timeout=60)

        self.add_item(AddBirthdayButton())
        self.add_item(DeleteBirthdayButton())
        self.add_item(BackButton(navigator=navigator))
