import discord


class Navigator:
    def __init__(self):
        self.routes = {
            'main_menu': self._main_menu_view,
            'admin_menu': self._admin_menu_view,
            'birthday_menu': self._admin_menu_view,
            'delete_msg_menu': self._delete_msg_menu_view,
            'superusers_menu': self._delete_msg_menu_view,
            'random_menu': self._random_menu_view,
            'role_manager_menu': self._role_manager_menu_view
        }

    def go(self, target: str, **params):
        try:
            return self.routes[target](**params)
        except KeyError:
            raise ValueError(f'Unknown target: {target}')

    def _main_menu_view(self, *, guild: discord.Guild, user_id: int):
        from modules.buttons.main_button_view import MainMenuView
        return MainMenuView(
                navigator=self,
                guild=guild,
                user_id=user_id
            )

    def _admin_menu_view(self, *, guild_id: int):
        from modules.buttons.for_admins.admin_menu_view import AdminMenuView
        return AdminMenuView(navigator=self, guild_id=guild_id)

    def _birthday_menu_view(self):
        from modules.buttons.for_admins.birthday_buttons.menu_view import BirthdayMenuView
        print('Створення BirthdayMenuView')
        return BirthdayMenuView(navigator=self)

    def _delete_msg_menu_view(self):
        from modules.buttons.for_admins.delete_message_buttons.menu_view import DeleteMsgMenuView
        print('Створення DeleteMsgMenuView')
        return DeleteMsgMenuView(navigator=self)

    def _superusers_menu_view(self):
        from modules.buttons.for_admins.superusers_buttons.menu_view import SuperusersMenuView
        print('Створення SuperusersMenuView')
        return SuperusersMenuView(navigator=self)

    def _random_menu_view(self):
        from modules.buttons.for_users.randomizer.menu_view import RandomModeView
        print('Створення RandomModeView')
        return RandomModeView(navigator=self)

    def _role_manager_menu_view(self):
        from modules.buttons.for_users.role_manager.menu_view import RoleManagerView
        print('Створення RoleManagerView')
        return RoleManagerView(navigator=self)
