from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings_manager import StorageTarget

from features.for_admins.admin_menu import AdminMenuButton
from features.for_everyone.birthdays.buttons import BirthdayMenuButton
from features.for_everyone.randomizer.buttons import RandomizerMenuButton
from features.for_everyone.role_manager.buttons import RoleManagerMenuButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from database.settings_storage.settings import SettingsStorage
    from features.for_everyone.birthdays.service import BirthdayService
    from ui.button_protection.button_protection_service import ButtonProtectionService
    from general_services.translator.translator import Translator


class MainMenuView(discord.ui.View):
    def __init__(
            self,
            settings: SettingsStorage,
            navigator: Navigator,
            buttons_protection: ButtonProtectionService,
            birthday_service: BirthdayService,
            context: NavigationContext,
            translator: Translator,
            guild_id: int,
            user_id: int,
            owner_id: int
    ):
        super().__init__(timeout=60)

        superusers = settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=guild_id
        )

        config = settings.dict_storage.get_all(
            target=StorageTarget.SETTINGS,
            guild_id=guild_id
        )

        role_manager = settings.dict_storage.get_value(
            'role_manager',
            target=StorageTarget.SETTINGS,
            guild_id=guild_id
        )

        self.add_item(
            RandomizerMenuButton(
                navigator=navigator,
                context=context,
                translator=translator,
                guild_id=guild_id
            )
        )

        if role_manager:
            self.add_item(
                RoleManagerMenuButton(
                    navigator=navigator,
                    context=context,
                    translator=translator,
                    guild_id=guild_id
                )
            )

        if config.get('birthday', False):
            self.add_item(
                BirthdayMenuButton(
                    navigator=navigator,
                    context=context,
                    service=birthday_service,
                    translator=translator,
                    guild_id=guild_id
                )
            )

        if user_id in superusers or user_id == owner_id:
            self.add_item(
                AdminMenuButton(
                    navigator=navigator,
                    context=context,
                    buttons_protection=buttons_protection,
                    translator=translator,
                    guild_id=guild_id
                )
            )
