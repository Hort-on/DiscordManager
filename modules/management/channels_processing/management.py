from discord.ui import View

from database.db_factory.db_scenario_factory import DBScenarioFactory
from database.settings_storage.settings_storage import SettingsStorage
from modules.birthdays.birthday_repo import BirthdayRepo

from modules.buttons.buttons_for_admins.birthday_button.views.add_birthday_view import AddBirthdayButton
from modules.buttons.buttons_for_admins.birthday_button.views.delete_birthday_view import DeleteBirthdayButton
from modules.buttons.buttons_for_admins.delete_message_button.delete_any_message.view.delete_message_view import \
    DeleteMessageButton
from modules.buttons.buttons_for_admins.edit_settings_button.views.edit_settings_view import EditSettingsButton
from modules.buttons.buttons_for_users.randomizer_button.view.randomizer_view import RandomizeButton
from modules.buttons.buttons_for_admins.send_message_button.view.send_message import SendMessageButton

from modules.logger.logger import Logger


class Management(View):
    def __init__(
            self,
            guild_id: int,
            settings: SettingsStorage,
            db_factory: DBScenarioFactory,
            birthday: BirthdayRepo,
            logger: Logger
    ):

        super().__init__()
        self.db_factory = db_factory
        self.guild_id = guild_id
        self.settings = settings
        self.birthday = birthday
        self.logger = logger

        self._add_buttons()

    def _add_buttons(self):
        """Додає кнопки залежно від налаштувань"""
        self.add_item(EditSettingsButton(self.db_factory))
        self.add_item(DeleteMessageButton())
        self.add_item(RandomizeButton()) #TODO: зробити загально доступною

        if self.settings.get_guild_settings(self.guild_id).get('birthday'):
            self.add_item(AddBirthdayButton(self.birthday))
            self.add_item(DeleteBirthdayButton(self.birthday))

        if self.settings.get_guild_settings(self.guild_id).get('send_messages'):
            self.add_item(SendMessageButton(self.db_factory))
