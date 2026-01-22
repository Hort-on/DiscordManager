from __future__ import annotations

import discord

from database.settings_storage.settings_manager import StorageTarget

from modules.buttons.for_admins.birthday_buttons.menu import BirthdayMenuButton
from modules.buttons.for_admins.delete_message_buttons.menu import DeleteMsgMenuButton
from modules.buttons.for_admins.superusers_buttons.menu import SuperusersMenuButton
from modules.buttons.for_admins.edit_settings_buttons.edit_settings import EditSettingsButton
from modules.buttons.for_admins.send_message_buttons.send_msg import SendMessageButton
from modules.buttons.other_buttons.back import BackButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.buttons.navigator import Navigator
    from database.settings_storage.settings import SettingsStorage


class AdminMenuView(discord.ui.View):
    def __init__(
            self,
            settings: SettingsStorage,
            navigator: Navigator,
            guild_id: int
    ):
        super().__init__(timeout=60)

        config = settings.dict_storage.for_dict_get_all(
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

        self.add_item(BackButton(target='main_menu', navigator=navigator))
