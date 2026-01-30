from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator

import discord

from modules.buttons.for_users.role_manager.buttons import AddRoleButton, RemoveRoleButton
from modules.buttons.other_buttons.back import BackButton


class RoleManagerView(discord.ui.View):
    def __init__(self, navigator: Navigator):
        super().__init__(timeout=60)

        self.add_item(AddRoleButton(navigator=navigator))
        self.add_item(RemoveRoleButton(navigator=navigator))

        self.add_item(BackButton(navigator=navigator))

