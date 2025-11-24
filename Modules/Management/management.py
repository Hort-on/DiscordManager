from discord.ui import View

from Modules.Management.buttons.birthday_view.add_birthday import AddBirthdayButton
from Modules.Management.buttons.birthday_view.delete_birthday import DeleteBirthdayButton
from Modules.Management.buttons.delete_message_view.delete_message import DeleteMessageButton
from Modules.Management.buttons.edit_settings_view.edit_settings_button import EditSettingsButton
from Modules.Management.buttons.send_message_view.send_message import SendMessageButton
from Modules.Management.buttons.set_permissions_view.set_permissions import SetPermissionButton


class Management(View):
    def __init__(self, ctx, bot, settings):
        super().__init__()
        self.ctx = ctx
        self.bot = bot
        self.settings = settings

        self._add_buttons()

    def _add_buttons(self):
        """Додає кнопки залежно від налаштувань"""
        self.add_item(EditSettingsButton(self.ctx))
        self.add_item(DeleteMessageButton(self.ctx))

        if self.settings.get("setting_permissions", False):
            self.add_item(SetPermissionButton(self.ctx))

        if self.settings.get('birthday', False):
            self.add_item(AddBirthdayButton(self.ctx))
            self.add_item(DeleteBirthdayButton(self.ctx))

        if self.settings.get('sending_messages', False):
            self.add_item(SendMessageButton(self.ctx))
