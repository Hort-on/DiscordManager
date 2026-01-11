from discord.ui import View

from database.settings_storage.settings_storage_manager import StorageTarget

from modules.buttons.general_buttons.buttons_for_admins.birthday_button.add_birthday_button import AddBirthdayButton
from modules.buttons.general_buttons.buttons_for_admins.birthday_button.delete_birthday_button import \
    DeleteBirthdayButton
from modules.buttons.general_buttons.buttons_for_admins.delete_message_button.delete_message_view import \
    DeleteMessageButton
from modules.buttons.general_buttons.buttons_for_admins.edit_settings_button.edit_settings_view import \
    EditSettingsButton
from modules.buttons.general_buttons.buttons_for_admins.send_message_button.send_message import SendMessageButton
from modules.buttons.general_buttons.buttons_for_users.random_buttons.first_random_view import RandomStartButton

from dependency_injector.wiring import inject, Provide
from core.bot_container import BotContainer


class ButtonManager(View):
    @inject
    def __init__(
            self,
            guild_id: int,
            birthday_manager=Provide[BotContainer.birthday_manager],
            settings=Provide[BotContainer.settings],
            db_factory=Provide[BotContainer.db_factory]
    ):

        super().__init__(timeout=60)
        self.guild_id = guild_id
        self.settings = settings
        self.db_factory = db_factory
        self.birthday_manager = birthday_manager

        self._add_buttons()

    def _add_buttons(self):
        """Додає кнопки залежно від налаштувань"""
        self.add_item(EditSettingsButton(self.db_factory, self.settings))
        self.add_item(DeleteMessageButton())
        self.add_item(RandomStartButton())

        if self.settings.dict_storage.get_for_dict(
                StorageTarget.SETTINGS,
                self.guild_id,
                'birthday'
        ):
            self.add_item(AddBirthdayButton(self.birthday_manager))
            self.add_item(DeleteBirthdayButton(self.birthday_manager))

        if self.settings.dict_storage.get_for_dict(
                StorageTarget.SETTINGS,
                self.guild_id,
                'send_messages'
        ):
            self.add_item(SendMessageButton(self.db_factory))
