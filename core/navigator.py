import discord


class Navigator:
    def __init__(self):
        self.routes = {
            'main_menu': self._main_menu,
            'admin_menu': self._admin_menu,
            'settings_menu': self._settings_menu,
            'birthday_menu': self._admin_menu,
            'delete_msg_menu': self._delete_msg_menu,
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

    def _main_menu(self, *, guild: discord.Guild, user_id: int):
        from features.for_everyone.main_menu import MainMenuView
        return MainMenuView(
                navigator=self,
                guild=guild,
                user_id=user_id
            )

    def _admin_menu(self, *, guild_id: int):
        from modules.buttons.for_admins.admin_menu_view import AdminMenuView
        return AdminMenuView(navigator=self, guild_id=guild_id)

    def _settings_menu(self):
        from modules.buttons.for_admins.edit_settings_buttons.menu_view import SettingsMenuView
        return SettingsMenuView(navigator=self)

    def _birthday_menu(self):
        from modules.buttons.for_admins.birthday_buttons.menu_view import BirthdayMenuView
        return BirthdayMenuView(navigator=self)

    def _delete_msg_menu(self):
        from modules.buttons.for_admins.delete_message_buttons.menu_view import DeleteMsgMenuView
        return DeleteMsgMenuView(navigator=self)

    def _superusers_menu(self):
        from modules.buttons.for_admins.superusers_buttons.menu_view import SuperusersMenuView
        return SuperusersMenuView(navigator=self)

    def _random_menu(self):
        from modules.buttons.for_users.randomizer.menu_view import RandomModeView
        return RandomModeView(navigator=self)

    def _role_manager_menu(self):
        from modules.buttons.for_users.role_manager.menu_view import RoleManagerView
        return RoleManagerView(navigator=self)

    def _hidden_channels_menu(self):
        from modules.buttons.for_admins.edit_settings_buttons.views import HiddenChannelsMenuView
        return HiddenChannelsMenuView(navigator=self)

    def _hidden_roles_menu(self):
        from modules.buttons.for_admins.edit_settings_buttons.views import HiddenRolesMenuView
        return HiddenRolesMenuView(navigator=self)

    def _system_channels_menu(self):
        from modules.buttons.for_admins.edit_settings_buttons.views import SystemChannelsMenuView
        return SystemChannelsMenuView(navigator=self)
