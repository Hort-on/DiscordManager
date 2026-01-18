from discord.ui import View

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget
from modules.birthdays.birthday_repo import BirthdayManager

from modules.buttons.for_users.randomizer.random_menu import RandomMenuButton
from modules.buttons.others.admin_menu import AdminMenuButton
from services.factories.db_factory.db_scenario_factory import DBFactory


class ButtonManager(View):
    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBFactory,
            birthday_manager: BirthdayManager,
            guild_id: int,
            user_id: int
    ):

        super().__init__(timeout=60)
        self.guild_id = guild_id
        self.user_id = user_id
        self.settings = settings
        self.db_factory = db_factory
        self.birthday_manager = birthday_manager

        self._add_buttons()

    def _add_buttons(self):
        superusers = self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=self.guild_id
        )

        self.add_item(RandomMenuButton(
            settings=self.settings,
            db_factory=self.db_factory,
            birthday_manager=self.birthday_manager
        ))

        if self.user_id in superusers:
            self._add_admin_panel()

    def _add_admin_panel(self):
        self.add_item(AdminMenuButton(
            settings=self.settings,
            db_factory=self.db_factory,
            birthday_manager=self.birthday_manager
        ))
