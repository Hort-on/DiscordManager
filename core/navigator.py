from __future__ import annotations

from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from features.for_admins.module import AdministrationModule
    from core.general_services_container import GeneralContainer


class Navigator:
    def __init__(
            self,
            general_container: GeneralContainer,
            admin_module: AdministrationModule
    ):
        self.admin_module = admin_module
        self.general_container = general_container
        self.routes = {
            'main_menu': self._main_menu,
            'admin_menu': self._admin_menu,
            'settings_menu': self._settings_menu,
            'birthday_menu': self._admin_menu,
            'superusers_menu': self._superusers_menu,
            'random_menu': self._random_menu,
            'role_manager_menu': self._role_manager_menu,

            'hidden_channels_menu': self._hidden_channels_menu,
            'hidden_roles_menu': self._hidden_roles_menu,
            'system_channels_menu': self._system_channels_menu,
        }

    def go(self, target: str, **params):
        view_factory = self.routes.get(target)

        if params:
            return view_factory(**params)
        return view_factory()

    def _main_menu(
            self,
            *,
            guild: discord.Guild,
            user_id: int,
    ):
        from features.for_everyone.main_menu.view import MainMenuView
        return MainMenuView(
                settings=self.general_container.settings,
                navigator=self,
                guild=guild,
                user_id=user_id
            )

    def _admin_menu(self, *, guild_id: int):
        from features.for_admins.admin_menu_view import AdminMenuView
        return AdminMenuView(
            navigator=self,
            settings=self.general_container.settings,
            superusers_formatter=self.admin_module.superusers_module.superusers_formatter,
            delete_msg_service=self.admin_module.delete_msg_module.delete_msg_service,
            send_msg_service=self.admin_module.send_message_module.send_message_service,
            guild_id=guild_id
        )

    def _settings_menu(self):
        from features.for_admins.edit_settings.menu_view import SettingsMenuView
        edit_settings_container = self.admin_module.edit_main_settings_module

        return SettingsMenuView(
            navigator=self,
            main_settings_service=edit_settings_container.main_settings_service,
            settings_formatter=edit_settings_container.settings_formatter_service
        )

    def _birthday_menu(self):
        from features.for_everyone.birthdays.menu_view import BirthdayMenuView
        return BirthdayMenuView(
            navigator=self
        )

    def _superusers_menu(self):
        from features.for_admins.superusers.menu_view import SuperusersMenuView
        return SuperusersMenuView(
            navigator=self,
            superusers_service=self.admin_module.superusers_module.superusers_service,
            formatter=self.admin_module.superusers_module.superusers_formatter
        )

    def _random_menu(self):
        from features.for_everyone.randomizer.menu_view import RandomModeView
        return RandomModeView(
            navigator=self
        )

    def _role_manager_menu(self):
        from features.for_everyone.role_manager.menu_view import RoleManagerView
        return RoleManagerView(
            navigator=self
        )

    def _hidden_channels_menu(self):
        from features.for_admins.edit_settings.views import HiddenChannelsMenuView
        edit_settings_container = self.admin_module.edit_main_settings_module

        return HiddenChannelsMenuView(
            navigator=self,
            hidden_ch_service=edit_settings_container.hidden_channel_service,
            formatter=edit_settings_container.formatter,
            cleanup_service=self.general_container.cleanup_service
        )

    def _hidden_roles_menu(self):
        from features.for_admins.edit_settings.views import HiddenRolesMenuView
        edit_settings_container = self.admin_module.edit_main_settings_module
        return HiddenRolesMenuView(
            navigator=self,
            formatter=edit_settings_container.formatter,
            hidden_roles_service=edit_settings_container.hidden_roles_service,
            cleanup_service=self.general_container.cleanup_service
        )

    def _system_channels_menu(self):
        from features.for_admins.edit_settings.views import SystemChannelsMenuView
        edit_settings_container = self.admin_module.edit_main_settings_module

        return SystemChannelsMenuView(
            navigator=self,
            sys_channels_service=edit_settings_container.system_channels_service,
            formatter=edit_settings_container.formatter
        )
