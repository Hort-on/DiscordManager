from discord.ui import View

from database.settings_storage.settings_storage import SettingsStorage

from services.factories.db_factory.db_scenario_factory import DBScenarioFactory

from modules.birthdays.birthday_repo import BirthdayRepo
from modules.logger.logger import Logger

from modules.buttons.buttons_for_admins.birthday_button.add_birthday_view import AddBirthdayButton
from modules.buttons.buttons_for_admins.birthday_button.delete_birthday_view import DeleteBirthdayButton
from modules.buttons.buttons_for_admins.edit_settings_button.edit_settings_view import EditSettingsButton
from modules.buttons.buttons_for_admins.send_message_button.send_message import SendMessageButton
from modules.buttons.buttons_for_admins.delete_message_button.delete_message_view import \
    DeleteMessageButton

from modules.buttons.buttons_for_users.randomizer_buttons.first_random_view import RandomizerStartButton


class Management(View):
    def __init__(
            self,
            guild_id: int,
            settings: SettingsStorage,
            db_factory: DBScenarioFactory,
            birthday: BirthdayRepo,
            logger: Logger
    ):

        super().__init__(timeout=60)
        self.db_factory = db_factory
        self.guild_id = guild_id
        self.settings = settings
        self.birthday = birthday
        self.logger = logger

        self._add_buttons()

    def _add_buttons(self):
        """Додає кнопки залежно від налаштувань"""
        self.add_item(EditSettingsButton(self.db_factory, self.settings))
        self.add_item(DeleteMessageButton())
        self.add_item(RandomizerStartButton())  # TODO: зробити загально доступною

        if self.settings.get_guild_settings(self.guild_id).get('birthday'):
            self.add_item(AddBirthdayButton(self.birthday))
            self.add_item(DeleteBirthdayButton(self.birthday))

        if self.settings.get_guild_settings(self.guild_id).get('send_messages'):
            self.add_item(SendMessageButton(self.db_factory))
