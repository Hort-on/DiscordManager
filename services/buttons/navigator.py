import discord

from services.buttons.render import Render
from services.factories.db_factory.db_scenario_factory import DBFactory
from services.yes_no_service.yes_no_factory import YesNoViewFactory


class Navigator:
    def go(self, target: str, **params) -> Render:
        match target:
            case 'main_menu':
                return self._render_main_menu(**params)

            case 'admin_menu':
                return self._render_admin_menu(**params)

            case 'edit_settings':
                return self._render_edit_settings(**params)

            case 'birthday_menu':
                return self._render_birthday_menu()

            case 'delete_msg_menu':
                return self._render_delete_msg_menu()

            case 'superusers_menu':
                return self._render_superusers_menu()

            case 'random_menu':
                return self._render_random_menu()

            case 'role_manager_menu':
                return self._render_role_manager_menu()

            case _:
                raise ValueError('Unknow target')

    def _render_main_menu(
            self,
            *,
            guild: discord.Guild,
            user_id: int,
    ) -> Render:
        from modules.buttons.main_button_view import MainMenuView

        return Render(
            view=MainMenuView(
                navigator=self,
                guild=guild,
                user_id=user_id
            )
        )

    def _render_admin_menu(self, *, guild_id: int) -> Render:
        from modules.buttons.for_admins.admin_menu_view import AdminMenuView

        return Render(
            view=AdminMenuView(navigator=self, guild_id=guild_id))

    def _render_edit_settings(
            self,
            *,
            db_factory: DBFactory,
            yes_no_factory: YesNoViewFactory
    ) -> Render:
        from modules.buttons.for_admins.edit_settings_buttons.services import SettingSelectorView

        return Render(
            view=SettingSelectorView(
                navigator=self,
                db_factory=db_factory,
                yes_no_factory=yes_no_factory
            )
        )

    def _render_birthday_menu(self):
        from modules.buttons.for_admins.birthday_buttons.menu_view import BirthdayMenuView

        return Render(view=BirthdayMenuView(navigator=self))

    def _render_delete_msg_menu(self):
        from modules.buttons.for_admins.delete_message_buttons.menu_view import DeleteMsgMenuView

        return Render(view=DeleteMsgMenuView(navigator=self))

    def _render_superusers_menu(self):
        from modules.buttons.for_admins.superusers_buttons.menu_view import SuperusersMenuView

        return Render(view=SuperusersMenuView(navigator=self))

    def _render_random_menu(self):
        from modules.buttons.for_users.randomizer.menu_view import RandomModeView

        return Render(view=RandomModeView(navigator=self))

    def _render_role_manager_menu(self):
        from modules.buttons.for_users.role_manager.menu_view import RoleManagerView

        return Render(view=RoleManagerView(navigator=self))

        #     case 'edit_settings':
        #         from modules.buttons.for_admins.edit_settings_buttons.services import SettingSelectorView
        #         formatter = SettingsFormatter()
        #         embed = await formatter.format_settings(interaction)
        #
        #         view = SettingSelectorView(
        #             navigator=self,
        #             db_factory=self.container.db_factory,
        #             yes_no_factory=self.container.yes_no_factory
        #         )
        #
        #         await interaction.edit_original_response(
        #             embed=embed,
        #             view=view
        #         )
        #         return Render(view=SettingSelectorView(navigator=self))
