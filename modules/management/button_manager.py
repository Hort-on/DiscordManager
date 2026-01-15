from discord.ui import View

from database.settings_storage.settings_manager import StorageTarget

from dependency_injector.wiring import inject, Provide

from core.bot_container import BotContainer

from modules.buttons.for_users.randomizer.random_menu import RandomMenuButton
from modules.buttons.others.admin_menu import AdminMenuButton


class ButtonManager(View):
    @inject
    def __init__(
            self,
            guild_id: int,
            user_id: int,
            settings=Provide[BotContainer.settings],
    ):

        super().__init__(timeout=60)
        self.guild_id = guild_id
        self.user_id = user_id
        self.settings = settings

        self._add_buttons()

    def _add_buttons(self):
        superusers = self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=self.guild_id
        )

        self.add_item(RandomMenuButton())

        if self.user_id in superusers:
            self._add_admin_panel()

    def _add_admin_panel(self):
        self.add_item(AdminMenuButton())
