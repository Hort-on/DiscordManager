from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.navigator import Navigator
    from database.settings_storage.settings import SettingsStorage

import discord

from database.settings_storage.settings_manager import StorageTarget

from modules.buttons.for_users.randomizer.menu import RandomMenuButton
from modules.buttons.for_admins.admin_menu import AdminMenuButton
from modules.buttons.for_users.role_manager.menu import RoleManagerMenuButton


class MainMenuView(discord.ui.View):
    def __init__(
            self,
            settings: SettingsStorage,
            navigator: Navigator,
            guild: discord.Guild,
            user_id: int
    ):
        super().__init__(timeout=60)

        superusers = settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=guild.id
        )

        role_manager = settings.dict_storage.for_dict_get(
            'role_manager',
            target=StorageTarget.SETTINGS,
            guild_id=guild.id
        )

        self.add_item(RandomMenuButton(navigator=navigator))

        if role_manager.get('role_manager'):
            self.add_item(RoleManagerMenuButton(navigator=navigator))

        if user_id in superusers or user_id == guild.owner_id:
            self.add_item(AdminMenuButton(navigator=navigator))
