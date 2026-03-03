from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.routes import Route

from features.for_admins.edit_settings.flows.hidden_roles import HiddenRolesFlow

from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from general_services.other_services.cleanup_service import CleanUpService
    from features.for_admins.edit_settings.services.hidden_roles import HiddenRolesService
    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter
    from ui.button_protection.button_protection_service import ButtonProtectionService


class HiddenRolesMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            context: NavigationContext,
            buttons_protection: ButtonProtectionService,
            formatter: SettingsFormatter,
            hidden_roles_service: HiddenRolesService,
            cleanup_service: CleanUpService
    ):
        super().__init__(
            label='Hidden roles management',
            style=discord.ButtonStyle.secondary,
            protection_service=buttons_protection
        )

        self.navigator = navigator
        self.context = context
        self.formatter = formatter
        self.hidden_roles_service = hidden_roles_service
        self.cleanup_service = cleanup_service

    async def on_click(self, interaction: discord.Interaction) -> None:
        view = self.navigator.hidden_roles_menu(context=self.context)

        view.context = self.context
        self.context.push(target=Route.SETTINGS_MENU)

        await interaction.response.edit_message(view=view)


class AddHiddenRoleButton(FirewallButton):
    scope = 'admin'

    def __init__(self, buttons_protection: ButtonProtectionService, flow: HiddenRolesFlow):
        super().__init__(
            label='📥Add hidden roles',
            style=discord.ButtonStyle.green,
            protection_service=buttons_protection
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.start_for_add(interaction=interaction)


class DeleteHiddenRoleButton(FirewallButton):
    scope = 'admin'

    def __init__(self, buttons_protection: ButtonProtectionService, flow: HiddenRolesFlow):
        super().__init__(
            label='🗑️Delete hidden roles',
            style=discord.ButtonStyle.red,
            protection_service=buttons_protection
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.start_for_delete(interaction=interaction)


class HiddenRolesListButton(FirewallButton):
    scope = 'admin'

    def __init__(self, buttons_protection: ButtonProtectionService, flow: HiddenRolesFlow):
        super().__init__(
            label='📄Hidden roles list',
            style=discord.ButtonStyle.blurple,
            protection_service=buttons_protection
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.for_roles_list(interaction=interaction)
