from __future__ import annotations

import discord

from modules.buttons.for_admins.superusers_buttons.buttons import (
    AddSuperuserButton,
    DeleteSuperusersButton,
    SuperusersListButton
)

from modules.buttons.other_buttons.back import BackButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.buttons.navigator import Navigator


class SuperusersMenuView(discord.ui.View):
    def __init__(self, navigator: Navigator):
        super().__init__(timeout=60)

        self.add_item(AddSuperuserButton())
        self.add_item(DeleteSuperusersButton())
        self.add_item(SuperusersListButton())
        self.add_item(BackButton(back_view=lambda: ))
