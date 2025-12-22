from discord.ui import View

from modules.buttons.buttons_for_admins.birthday_button.views.add_birthday_view import AddBirthdayButton
from modules.buttons.buttons_for_admins.birthday_button.views.delete_birthday_view import DeleteBirthdayButton
from modules.buttons.buttons_for_admins.delete_message_button.delete_any_message.view import DeleteMessageButton
from modules.buttons.buttons_for_admins.edit_settings_button.views.edit_settings_view import EditSettingsButton
from modules.buttons.buttons_for_users.randomizer_button.view.randomizer_view import RandomizeButton
from modules.buttons.buttons_for_admins.send_message_button.view.send_message import SendMessageButton
from modules.buttons.buttons_for_admins.set_permissions_button.view.set_permissions_view import SetPermissionButton


class Management(View):
    def __init__(self, ctx, bot, settings):
        super().__init__()
        self.ctx = ctx
        self.bot = bot
        self.settings = settings

        self._add_buttons()

    def _add_buttons(self):
        """Додає кнопки залежно від налаштувань"""
        self.add_item(EditSettingsButton())
        self.add_item(DeleteMessageButton())
        self.add_item(RandomizeButton()) #TODO: зробити загально доступною

        if self.settings.get("setting_permissions", False):
            self.add_item(SetPermissionButton())

        if self.settings.get('birthday', False):
            self.add_item(AddBirthdayButton())
            self.add_item(DeleteBirthdayButton())

        if self.settings.get('sending_messages', False):
            self.add_item(SendMessageButton())
