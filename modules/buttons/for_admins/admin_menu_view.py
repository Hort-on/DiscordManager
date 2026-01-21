import discord

from core.bot_container import AppContainer
from core.main import BotController

from database.settings_storage.settings_manager import StorageTarget

from modules.buttons.main_button_view import MainButtonView

from modules.buttons.for_admins.birthday_buttons.menu import BirthdayMenuButton
from modules.buttons.for_admins.delete_message_buttons.menu import DeleteMsgMenuButton
from modules.buttons.for_admins.superusers_buttons.menu import SuperusersMenuButton
from modules.buttons.for_admins.edit_settings_buttons.edit_settings import EditSettingsButton
from modules.buttons.for_admins.send_message_buttons.send_msg import SendMessageButton
from modules.buttons.other_buttons.back import BackButton


class AdminMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        controller: BotController = AppContainer.get()

        self.settings = controller.settings

    def prepare(self, guild_id: int, user_id: int):
        config = self.settings.dict_storage.for_dict_get_all(
            target=StorageTarget.SETTINGS,
            guild_id=guild_id
        )

        self.add_item(EditSettingsButton())
        self.add_item(SuperusersMenuButton())
        self.add_item(DeleteMsgMenuButton())

        if config.get('birthday'):
            self.add_item(BirthdayMenuButton())

        if config.get('send_messages'):
            self.add_item(SendMessageButton())

        self.add_item(BackButton(
            back_view=lambda: MainButtonView().prepare(
                guild_id=guild_id,
                user_id=user_id
            )
        ))

        return self
