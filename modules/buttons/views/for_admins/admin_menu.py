import discord

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

from modules.birthdays.birthday_repo import BirthdayManager

from modules.management.button_manager import ButtonManager

from modules.buttons.for_admins.birthday_buttons.birthday_menu import BirthdayMenuButton
from modules.buttons.for_admins.delete_message.delete_msg_menu import DeleteMsgMenuButton
from modules.buttons.for_admins.superusers_button.superusers_menu import SuperusersMenuButton
from modules.buttons.for_admins.edit_settings_button.edit_settings import EditSettingsButton
from modules.buttons.for_admins.send_message_button.send_msg import SendMessageButton
from modules.buttons.others.back import BackButton

from services.factories.db_factory.db_scenario_factory import DBFactory


class AdminMenuView(discord.ui.View):
    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBFactory,
            birthday_manager: BirthdayManager,
            guild_id: int,
            user_id: int
    ):

        super().__init__(timeout=60)
        self.settings = settings
        self.db_factory = db_factory
        self.birthday_manager = birthday_manager
        self.guild_id = guild_id
        self.user_id = user_id

        self._add_buttons()

    def _add_buttons(self):
        config = self.settings.dict_storage.for_dict_get_all(
            target=StorageTarget.SETTINGS,
            guild_id=self.guild_id
        )

        self.add_item(EditSettingsButton(settings=self.settings, db_factory=self.db_factory,))
        self.add_item(SuperusersMenuButton(settings=self.settings, db_factory=self.db_factory))
        self.add_item(DeleteMsgMenuButton(guild_id=self.guild_id, user_id=self.user_id))

        if config.get('birthday'):
            self.add_item(BirthdayMenuButton(birthday_manager=self.birthday_manager))

        if config.get('send_messages'):
            self.add_item(SendMessageButton(db_factory=self.db_factory))

        self.add_item(BackButton(
            back_view=lambda: ButtonManager(
                settings=self.settings,
                db_factory=self.db_factory,
                birthday_manager=self.birthday_manager,
                guild_id=self.guild_id,
                user_id=self.user_id
            )))
