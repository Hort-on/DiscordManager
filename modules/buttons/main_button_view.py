from __future__ import annotations

import discord

from database.settings_storage.settings_manager import StorageTarget

from modules.buttons.for_users.randomizer.menu import RandomMenuButton
from modules.buttons.for_admins.admin_menu import AdminMenuButton
from modules.buttons.for_users.role_manager.menu import RoleManagerMenuButton

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.buttons.navigator import Navigator
    from database.settings_storage.settings import SettingsStorage


class MainMenuView(discord.ui.View):
    def __init__(
            self,
            settings: SettingsStorage,
            navigator: Navigator,
            guild_id: int,
            user_id: int
    ):
        super().__init__(timeout=60)

        superusers = settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=guild_id
        )

        self.add_item(RandomMenuButton(navigator=navigator))
        self.add_item(RoleManagerMenuButton(navigator=navigator))

        if user_id in superusers:
            self.add_item(AdminMenuButton(navigator=navigator))

