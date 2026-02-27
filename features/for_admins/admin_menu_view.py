from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings_manager import StorageTarget

from features.for_admins.delete_message.buttons import DeleteMessageButton
from features.for_admins.edit_settings.menu_button import EditSettingsMenuButton
from features.for_admins.send_anon_messages.button import SendMessageButton
from features.for_admins.superusers.buttons import SuperusersMenuButton

from ui.buttons.back_button import BackButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from database.settings_storage.settings import SettingsStorage
    from features.for_admins.superusers.formatter import SuperusersFormatter
    from features.for_admins.delete_message.service import DeleteMessageService
    from features.for_admins.send_anon_messages.service import SendAnonMessageService
    from features.for_admins.superusers.services import SuperusersService
    from ui.button_protection.button_protection_service import ButtonProtectionService


class AdminMenuView(discord.ui.View):
    def __init__(
        self,
        navigator: Navigator,
        settings: SettingsStorage,
        superusers_formatter: SuperusersFormatter,
        buttons_protection: ButtonProtectionService,
        delete_msg_service: DeleteMessageService,
        send_msg_service: SendAnonMessageService,
        superusers_service: SuperusersService,
        guild_id: int
    ):
        super().__init__(timeout=60)

        config = settings.dict_storage.for_dict_get(
            target=StorageTarget.SETTINGS,
            guild_id=guild_id
        )

        self.add_item(SuperusersMenuButton(
            navigator=navigator,
            formatter=superusers_formatter,
            superusers_service=superusers_service,
            buttons_protection=buttons_protection
        ))
        self.add_item(DeleteMessageButton(
            navigator=navigator,
            delete_msg_service=delete_msg_service,
            buttons_protection=buttons_protection
        ))
        self.add_item(EditSettingsMenuButton(
            navigator=navigator,
            buttons_protection=buttons_protection
        ))

        if config.get('send_messages'):
            self.add_item(SendMessageButton(
                navigator=navigator,
                service=send_msg_service,
                buttons_protection=buttons_protection
            ))

        self.add_item(BackButton(navigator=navigator))
