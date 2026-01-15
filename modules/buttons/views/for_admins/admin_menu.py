import discord

from dependency_injector.wiring import inject, Provide

from core.bot_container import BotContainer

from database.settings_storage.settings_manager import StorageTarget

from modules.management.button_manager import ButtonManager

from modules.buttons.for_admins.birthday_buttons.birthday_menu import BirthdayMenuButton
from modules.buttons.for_admins.delete_message.delete_msg_menu import DeleteMsgMenuButton
from modules.buttons.for_admins.superusers_button.superusers_menu import SuperusersMenuButton
from modules.buttons.for_admins.edit_settings_button.edit_settings import EditSettingsButton
from modules.buttons.for_admins.send_message_button.send_msg import SendMessageButton
from modules.buttons.others.back import BackButton


class AdminMenuView(discord.ui.View):
    @inject
    def __init__(
            self,
            guild_id: int,
            user_id: int,
            settings=Provide[BotContainer.settings],
            db_factory=Provide[BotContainer.db_factory],
            birthday_manager=Provide[BotContainer.birthday_manager]
    ):

        super().__init__(timeout=60)
        self.guild_id = guild_id
        self.user_id = user_id
        self.settings = settings
        self.db_factory = db_factory
        self.birthday_manager = birthday_manager

        self._add_buttons()

    def _add_buttons(self):
        config = self.settings.dict_storage.get_for_dict_all(
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
            view_factory=lambda: ButtonManager(
                guild_id=self.guild_id,
                user_id=self.user_id
            )))
