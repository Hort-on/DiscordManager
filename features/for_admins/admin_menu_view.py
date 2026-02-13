from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.navigator import Navigator
    from database.settings_storage.settings import SettingsStorage

import discord

from database.settings_storage.settings_manager import StorageTarget

from modules.buttons.for_admins.birthday_buttons.menu import BirthdayMenuButton
from modules.buttons.for_admins.delete_message_buttons.menu import DeleteMsgMenuButton
from modules.buttons.for_admins.superusers_buttons.menu import SuperusersMenuButton
from modules.buttons.for_admins.edit_settings_buttons.menu_button import EditSettingsMenuButton
from modules.buttons.for_admins.send_message_buttons.send_msg import SendMessageButton
from modules.buttons.other_buttons.back import BackButton


class AdminMenuView(discord.ui.View):
    def __init__(
        self,
        navigator: Navigator,
        settings: SettingsStorage,
        guild_id: int
    ):
        super().__init__(timeout=60)

        config = settings.dict_storage.for_dict_get(
            target=StorageTarget.SETTINGS,
            guild_id=guild_id
        )

        self.add_item(SuperusersMenuButton(navigator=navigator))
        self.add_item(DeleteMsgMenuButton(navigator=navigator))
        self.add_item(EditSettingsMenuButton(navigator=navigator))

        if config.get('birthday'):
            self.add_item(BirthdayMenuButton(navigator=navigator))

        if config.get('send_messages'):
            self.add_item(SendMessageButton(navigator=navigator))

        self.add_item(BackButton(navigator=navigator))
