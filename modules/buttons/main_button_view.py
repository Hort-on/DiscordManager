from __future__ import annotations

import discord

from modules.buttons.for_users.randomizer.menu import RandomMenuButton
from modules.buttons.for_admins.admin_menu import AdminMenuButton
from modules.buttons.for_users.role_manager.menu import RoleManagerMenuButton

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.buttons.navigator import Navigator


class MainMenuView(discord.ui.View):
    def __init__(
            self,
            superusers: set[int],
            navigator: Navigator,
            guild: discord.Guild,
            user_id: int
    ):
        super().__init__(timeout=60)

        self.add_item(RandomMenuButton(navigator=navigator))
        self.add_item(RoleManagerMenuButton(navigator=navigator))

        if user_id in superusers or user_id == guild.owner_id:
            self.add_item(AdminMenuButton(navigator=navigator))
