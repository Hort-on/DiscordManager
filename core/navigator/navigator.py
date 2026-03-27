from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import asdict

from .routes import Route

if TYPE_CHECKING:
    from core.general_services_container import GeneralContainer
    from features.for_admins.module import AdministrationModule
    from features.for_everyone.module import EveryoneModule
    from core.navigator.navigator_context import NavigationContext


class Navigator:
    def __init__(
            self,
            general_container: GeneralContainer,
            admin_module: AdministrationModule,
            everyone_module: EveryoneModule
    ):
        self.general_container = general_container
        self.admin_module = admin_module
        self.everyone_module = everyone_module

        self.routes = {
            Route.MAIN_MENU: self.main_menu,
            Route.ADMIN_MENU: self.admin_menu,
            Route.SETTINGS_MENU: self.settings_menu,
            Route.BIRTHDAY_MENU: self.birthday_menu,
            Route.SUPERUSERS_MENU: self.superusers_menu,
            Route.RANDOMIZER_MENU: self.randomizer_menu,
            Route.ROLE_MANAGER_MENU: self.role_manager_menu,
            Route.HIDDEN_CHANNELS_MENU: self.hidden_channels_menu,
            Route.HIDDEN_ROLES_MENU: self.hidden_roles_menu,
            Route.SYSTEM_CHANNELS_MENU: self.system_channels_menu,
            Route.SEND_MESSAGE_MENU: self.send_message_menu,
        }

    def go(self, route: Route, context: NavigationContext, params=None):
        factory = self.routes.get(route)

        if params:
            return factory(**asdict(params), context=context)

        return factory(context=context)

    def main_menu(self, guild_id: int, user_id: int, owner_id: int, context: NavigationContext):
        from features.for_everyone.main_menu.view import MainMenuView
        birthday_module = self.everyone_module.birthday_module
        return MainMenuView(
                settings=self.general_container.settings,
                navigator=self,
                buttons_protection=self.general_container.button_protection,
                birthday_service=birthday_module.service,
                translator=self.general_container.translator,
                guild_id=guild_id,
                user_id=user_id,
                owner_id=owner_id,
                context=context
            )

    def admin_menu(self, guild_id: int, context: NavigationContext):
        from features.for_admins.admin_menu_view import AdminMenuView

        superusers_module = self.admin_module.superusers_module
        delete_msg_module = self.admin_module.delete_msg_module

        return AdminMenuView(
            navigator=self,
            context=context,
            settings=self.general_container.settings,
            translator=self.general_container.translator,
            superusers_formatter=superusers_module.superusers_formatter,
            delete_msg_service=delete_msg_module.delete_msg_service,
            protection_service=self.general_container.button_protection,
            guild_id=guild_id
        )

    def settings_menu(self, context: NavigationContext, guild_id: int):
        from features.for_admins.edit_settings.menu_view import SettingsMenuView
        edit_settings_container = self.admin_module.edit_main_settings_module

        return SettingsMenuView(
            navigator=self,
            context=context,
            main_settings_service=edit_settings_container.main_settings_service,
            settings_formatter=edit_settings_container.formatter,
            buttons_protection=self.general_container.button_protection,
            hidden_ch_service=edit_settings_container.hidden_channel_service,
            hidden_role_service=edit_settings_container.hidden_roles_service,
            cleanup_service=self.general_container.cleanup_service,
            service_for_role=self.admin_module.edit_main_settings_module.verification_role_service,
            translator=self.general_container.translator,
            guild_id=guild_id
        )

    def birthday_menu(self, guild_id: int):
        from features.for_everyone.birthdays.flow import BirthdayFlow
        from features.for_everyone.birthdays.menu_view import BirthdayMenuView

        flow = BirthdayFlow(
            navigator=self,
            service=self.everyone_module.birthday_module.service,
            translator=self.general_container.translator
        )

        return BirthdayMenuView(
            navigator=self,
            flow=flow,
            translator=self.general_container.translator,
            guild_id=guild_id
        )

    def superusers_menu(self, context: NavigationContext, guild_id: int):
        from features.for_admins.superusers.flow import SuperusersFlow
        from features.for_admins.superusers.menu_view import SuperusersMenuView

        superusers_module = self.admin_module.superusers_module

        flow = SuperusersFlow(
            navigator=self,
            context=context,
            superusers_service=superusers_module.superusers_service,
            formatter=superusers_module.superusers_formatter,
            translator=self.general_container.translator
        )

        return SuperusersMenuView(
            navigator=self,
            buttons_protection=self.general_container.button_protection,
            flow=flow,
            translator=self.general_container.translator,
            guild_id=guild_id
        )

    def randomizer_menu(self, guild_id: int):
        from features.for_everyone.randomizer.flow import RandomizerFlow
        from features.for_everyone.randomizer.menu_view import RandomModeView

        randomizer_module = self.everyone_module.randomizer_module

        flow = RandomizerFlow(
            navigator=self,
            service=randomizer_module.service,
            translator=self.general_container.translator
        )

        return RandomModeView(
            navigator=self,
            flow=flow,
            translator=self.general_container.translator,
            guild_id=guild_id
        )

    def role_manager_menu(self, context: NavigationContext, guild_id: int):
        from features.for_everyone.role_manager.flow import RoleManagerFlow
        from features.for_everyone.role_manager.menu_view import RoleManagerView

        role_manager_module = self.everyone_module.role_manager_module

        flow = RoleManagerFlow(
            navigator=self,
            context=context,
            service=role_manager_module.service,
            translator=self.general_container.translator
        )

        return RoleManagerView(
            navigator=self,
            flow=flow,
            translator=self.general_container.translator,
            guild_id=guild_id
        )

    def hidden_channels_menu(self, context: NavigationContext, guild_id: int):
        from features.for_admins.edit_settings.flows.hidden_channels import HiddenChannelsFlow
        from features.for_admins.edit_settings.views import HiddenChannelsMenuView

        edit_settings_container = self.admin_module.edit_main_settings_module

        flow = HiddenChannelsFlow(
            navigator=self,
            context=context,
            formatter=edit_settings_container.formatter,
            hidden_ch_service=edit_settings_container.hidden_channel_service,
            cleanup_service=self.general_container.cleanup_service,
            translator=self.general_container.translator
        )

        return HiddenChannelsMenuView(
            navigator=self,
            buttons_protection=self.general_container.button_protection,
            flow=flow,
            translator=self.general_container.translator,
            guild_id=guild_id
        )

    def hidden_roles_menu(self, context: NavigationContext, guild_id: int):
        from features.for_admins.edit_settings.flows.hidden_roles import HiddenRolesFlow
        from features.for_admins.edit_settings.views import HiddenRolesMenuView

        edit_settings_container = self.admin_module.edit_main_settings_module

        flow = HiddenRolesFlow(
            navigator=self,
            context=context,
            formatter=edit_settings_container.formatter,
            hidden_roles_service=edit_settings_container.hidden_roles_service,
            cleanup_service=self.general_container.cleanup_service,
            translator=self.general_container.translator
        )

        return HiddenRolesMenuView(
            navigator=self,
            buttons_protection=self.general_container.button_protection,
            flow=flow,
            translator=self.general_container.translator,
            guild_id=guild_id
        )

    def system_channels_menu(self, context: NavigationContext, guild_id: int):
        from features.for_admins.edit_settings.flows.sys_channels import SystemChannelsFlow
        from features.for_admins.edit_settings.views import SystemChannelsMenuView

        edit_settings_container = self.admin_module.edit_main_settings_module

        flow = SystemChannelsFlow(
            navigator=self,
            context=context,
            sys_channels_service=edit_settings_container.system_channels_service,
            formatter=edit_settings_container.formatter,
            translator=self.general_container.translator
        )

        return SystemChannelsMenuView(
            navigator=self,
            buttons_protection=self.general_container.button_protection,
            flow=flow,
            translator=self.general_container.translator,
            guild_id=guild_id
        )

    def send_message_menu(self, guild_id: int):
        from features.for_admins.send_messages.flows.send_message_flow import SendMessageFlow
        from features.for_admins.send_messages.flows.send_rules_flow import SendRulesFlow
        from features.for_admins.send_messages.view import SendMessageMenuView

        message_module = self.admin_module.message_module

        message_flow = SendMessageFlow(
            navigator=self,
            message_service=message_module.send_message_service,
            translator=self.general_container.translator
        )

        rules_fow = SendRulesFlow(
            navigator=self,
            rules_service=message_module.rules_service,
            translator=self.general_container.translator
        )

        return SendMessageMenuView(
            navigator=self,
            buttons_protection=self.general_container.button_protection,
            messages_flow=message_flow,
            rules_flow=rules_fow,
            translator=self.general_container.translator,
            guild_id=guild_id
        )
