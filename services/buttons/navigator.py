import discord

from services.factories.db_factory.db_scenario_factory import DBFactory
from services.yes_no_service.yes_no_factory import YesNoViewFactory


class Navigator:
    def go(self, target: str, **params):
        match target:
            case 'main_menu':
                print('Ми у кейсі: main_menu')
                return self._main_menu_view(**params)

            case 'admin_menu':
                print('Ми у кейсі: admin_menu')
                return self._admin_menu_view(**params)

            case 'edit_settings':
                print('Ми у кейсі: edit_settings')
                return self._edit_settings_view(**params)

            case 'birthday_menu':
                print('Ми у кейсі: birthday_menu')
                return self._birthday_menu_view()

            case 'delete_msg_menu':
                print('Ми у кейсі: delete_msg_menu')
                return self._delete_msg_menu_view()

            case 'superusers_menu':
                print('Ми у кейсі: superusers_menu')
                return self._superusers_menu_view()

            case 'random_menu':
                print('Ми у кейсі: random_menu')
                return self._random_menu_view()

            case 'role_manager_menu':
                print('Ми у кейсі: role_manager_menu')
                return self._role_manager_menu_view()

            case _:
                raise ValueError('Unknow target')

    def _main_menu_view(self, *, guild: discord.Guild, user_id: int):
        from modules.buttons.main_button_view import MainMenuView
        print('Створення MainMenuView')
        return MainMenuView(
                navigator=self,
                guild=guild,
                user_id=user_id
            )

    def _admin_menu_view(self, *, guild_id: int):
        from modules.buttons.for_admins.admin_menu_view import AdminMenuView
        print('Створення AdminMenuView')
        return AdminMenuView(navigator=self, guild_id=guild_id)

    def _edit_settings_view(
            self,
            *,
            db_factory: DBFactory,
            yes_no_factory: YesNoViewFactory
    ):
        from modules.buttons.for_admins.edit_settings_buttons.services import SettingSelectorView
        print('Створення SettingSelectorView')
        return SettingSelectorView(
                navigator=self,
                db_factory=db_factory,
                yes_no_factory=yes_no_factory
            )

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
