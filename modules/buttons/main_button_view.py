from __future__ import annotations

import discord

from core.container import AppContainer
from database.settings_storage.settings_manager import StorageTarget

from modules.buttons.for_users.randomizer.menu import RandomMenuButton
from modules.buttons.for_admins.admin_menu import AdminMenuButton
from modules.buttons.for_users.role_manager.menu import RoleManagerMenuButton

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator
    from core.container import BotContainer


class MainMenuView(discord.ui.View):
    def __init__(
            self,
            navigator: Navigator,
            guild: discord.Guild,
            user_id: int
    ):
        super().__init__(timeout=60)

        container: BotContainer = AppContainer.get()

        print('отримання супер користувачів у: MainMenuView')
        superusers = container.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=guild.id
        )

        print('Додаємо кнопку: RandomMenuButton')
        self.add_item(RandomMenuButton(navigator=navigator))
        print('Додаємо кнопку: RoleManagerMenuButton')
        self.add_item(RoleManagerMenuButton(navigator=navigator))

        if user_id in superusers or user_id == guild.owner_id:
            print('Додаємо кнопку: AdminMenuButton')
            self.add_item(AdminMenuButton(navigator=navigator))
