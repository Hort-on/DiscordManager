from discord.ui import View

from core.bot_container import AppContainer

from database.settings_storage.settings_manager import StorageTarget

from modules.buttons.for_users.randomizer.menu import RandomMenuButton
from modules.buttons.for_admins.admin_menu import AdminMenuButton
from modules.buttons.for_users.role_manager.menu import RoleManagerMenuButton


class MainButtonView(View):
    def __init__(self):
        super().__init__(timeout=60)

    def prepare(self, guild_id: int, user_id: int):
        container = AppContainer.get()

        superusers = container.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=guild_id
        )

        self.add_item(RandomMenuButton())
        self.add_item(RoleManagerMenuButton())

        if user_id in superusers:
            self.add_item(AdminMenuButton())

        return self
