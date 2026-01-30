from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator
    from core.container import BotContainer

import discord

from core.container import AppContainer

from database.settings_storage.settings_manager import StorageTarget

from modules.buttons.for_admins.birthday_buttons.menu import BirthdayMenuButton
from modules.buttons.for_admins.delete_message_buttons.menu import DeleteMsgMenuButton
from modules.buttons.for_admins.superusers_buttons.menu import SuperusersMenuButton
from modules.buttons.for_admins.edit_settings_buttons.edit_settings import EditSettingsButton
from modules.buttons.for_admins.send_message_buttons.send_msg import SendMessageButton
from modules.buttons.other_buttons.back import BackButton


class AdminMenuView(discord.ui.View):
    def __init__(
        self,
        navigator: Navigator,
        guild_id: int
    ):
        super().__init__(timeout=60)

        container: BotContainer = AppContainer.get()

        config = container.settings.dict_storage.for_dict_get_all(
            target=StorageTarget.SETTINGS,
            guild_id=guild_id
        )

        print('Додаємо кнопки')
        self.add_item(SuperusersMenuButton(navigator=navigator))
        print('Додали SuperusersMenuButton')
        self.add_item(DeleteMsgMenuButton(navigator=navigator))
        print('Додали DeleteMsgMenuButton')
        self.add_item(EditSettingsButton(navigator=navigator))
        print('Додали EditSettingsButton')

        if config.get('birthday'):
            self.add_item(BirthdayMenuButton(navigator=navigator))
            print('Додали BirthdayMenuButton')

        if config.get('send_messages'):
            self.add_item(SendMessageButton(navigator=navigator))
            print('Додали SendMessageButton')

        self.add_item(BackButton(navigator=navigator))
        print('Додали BackButton')
