from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings_manager import StorageTarget

from features.for_admins.admin_menu import AdminMenuButton
from features.for_everyone.birthdays.buttons import BirthdayMenuButton
from features.for_everyone.randomizer.buttons import RandomizerMenuButton
from features.for_everyone.role_manager.menu import RoleManagerMenuButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from database.settings_storage.settings import SettingsStorage
    from features.for_everyone.birthdays.service import BirthdayService
    from ui.button_protection.button_protection_service import ButtonProtectionService


class MainMenuView(discord.ui.View):
    def __init__(
            self,
            settings: SettingsStorage,
            navigator: Navigator,
            buttons_protection: ButtonProtectionService,
            birthday_service: BirthdayService,
            guild: discord.Guild,
            user_id: int,
    ):
        super().__init__(timeout=60)

        superusers = settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=guild.id
        )

        config = settings.dict_storage.for_dict_get(
            target=StorageTarget.SETTINGS,
            guild_id=guild.id
        )

        role_manager = settings.dict_storage.for_dict_get(
            'role_manager',
            target=StorageTarget.SETTINGS,
            guild_id=guild.id
        )

        self.add_item(RandomizerMenuButton(navigator=navigator))

        if role_manager.get('role_manager', False):
            self.add_item(RoleManagerMenuButton(navigator=navigator))

        if config.get('birthday', False):
            self.add_item(BirthdayMenuButton(
                navigator=navigator,
                service=birthday_service
            ))

        if user_id in superusers or user_id == guild.owner_id:
            self.add_item(AdminMenuButton(
                navigator=navigator,
                buttons_protection=buttons_protection
            ))
