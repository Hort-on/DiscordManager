from __future__ import annotations

import discord

from modules.buttons.for_users.role_manager.buttons import AddRoleButton, RemoveRoleButton
from modules.buttons.other_buttons.back import BackButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.buttons.navigator import Navigator


class RoleManagerView(discord.ui.View):
    def __init__(self, navigator: Navigator):
        super().__init__(timeout=60)

        self.add_item(AddRoleButton())
        self.add_item(RemoveRoleButton())

        self.add_item(BackButton(back_view=lambda:))

