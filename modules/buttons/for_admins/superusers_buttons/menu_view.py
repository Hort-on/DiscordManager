from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator

import discord

from modules.buttons.for_admins.superusers_buttons.buttons import (
    AddSuperuserButton,
    DeleteSuperusersButton,
    SuperusersListButton
)

from modules.buttons.other_buttons.back import BackButton


class SuperusersMenuView(discord.ui.View):
    def __init__(self, navigator: Navigator):
        super().__init__(timeout=60)

        self.add_item(AddSuperuserButton())
        self.add_item(DeleteSuperusersButton(navigator=navigator))
        self.add_item(SuperusersListButton())
        self.add_item(BackButton(navigator=navigator))
