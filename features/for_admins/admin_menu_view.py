from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings_manager import StorageTarget

from features.for_admins.delete_message.buttons import DeleteMessageButton
from features.for_admins.edit_settings.menu_button import EditSettingsMenuButton
from features.for_admins.send_anon_messages.send_msg import SendMessageButton
from features.for_admins.superusers.menu import SuperusersMenuButton
from features.for_everyone.birthdays.menu import BirthdayMenuButton

from ui.buttons.back_button import BackButton

if TYPE_CHECKING:
    from core.navigator import Navigator
    from database.settings_storage.settings import SettingsStorage


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
        self.add_item(DeleteMessageButton(navigator=navigator))
        self.add_item(EditSettingsMenuButton(navigator=navigator))

        if config.get('birthday'):
            self.add_item(BirthdayMenuButton(navigator=navigator))

        if config.get('send_messages'):
            self.add_item(SendMessageButton(navigator=navigator))

        self.add_item(BackButton(navigator=navigator))
