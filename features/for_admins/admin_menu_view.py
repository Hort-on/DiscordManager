from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings_manager import StorageTarget

from features.for_admins.delete_message.buttons import DeleteMessageButton
from features.for_admins.edit_settings.menu_button import EditSettingsMenuButton
from features.for_admins.send_messages.buttons import SendMessageMenu
from features.for_admins.superusers.buttons import SuperusersMenuButton

from ui.buttons.back_button import BackButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from database.settings_storage.settings import SettingsStorage
    from features.for_admins.superusers.formatter import SuperusersFormatter
    from features.for_admins.delete_message.service import DeleteMessageService
    from ui.button_protection.button_protection_service import ButtonProtectionService
    from general_services.translator.translator import Translator


class AdminMenuView(discord.ui.View):
    def __init__(
        self,
        navigator: Navigator,
        context: NavigationContext,
        settings: SettingsStorage,
        translator: Translator,
        superusers_formatter: SuperusersFormatter,
        protection_service: ButtonProtectionService,
        delete_msg_service: DeleteMessageService,
        guild_id: int
    ):
        super().__init__(timeout=60)

        config = settings.dict_storage.get_all(
            target=StorageTarget.SETTINGS,
            guild_id=guild_id
        )

        self.add_item(
            SuperusersMenuButton(
                navigator=navigator,
                context=context,
                formatter=superusers_formatter,
                buttons_protection=protection_service
            )
        )

        self.add_item(
            DeleteMessageButton(
                guild_id=guild_id,
                navigator=navigator,
                context=context,
                delete_msg_service=delete_msg_service,
                buttons_protection=protection_service,
                translator=translator
            )
        )

        self.add_item(
            EditSettingsMenuButton(
                navigator=navigator,
                context=context,
                buttons_protection=protection_service,
                translator=translator,
                guild_id=guild_id
            )
        )

        if config.get('send_messages'):
            self.add_item(
                SendMessageMenu(
                    navigator=navigator,
                    context=context,
                    protection_service=protection_service,
                    translator=translator,
                    guild_id=guild_id
                )
            )

        self.add_item(BackButton(navigator=navigator))
