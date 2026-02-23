from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.for_admins.edit_settings.flows.hidden_roles import HiddenRolesFlow

from core.navigator_context import NavigationContext

from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator import Navigator
    from general_services.other_services.cleanup_service import CleanUpService
    from features.for_admins.edit_settings.services.hidden_roles import HiddenRolesService
    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter
    from ui.button_protection.button_protection_service import ButtonProtectionService


class HiddenRolesMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator, buttons_protection: ButtonProtectionService):
        super().__init__(
            label='Hidden roles management',
            style=discord.ButtonStyle.secondary,
            service=buttons_protection
        )

        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:  # TODO: зробити через flow
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='settings_menu')

        view = self.navigator.go(target='hidden_roles_menu')

        view.context = context

        await interaction.response.edit_message(view=view)


class AddHiddenRoleButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            formatter: SettingsFormatter,
            hidden_roles_service: HiddenRolesService,
            cleanup_service: CleanUpService,
            buttons_protection: ButtonProtectionService
    ):
        super().__init__(
            label='📥Add hidden roles',
            style=discord.ButtonStyle.green,
            service=buttons_protection
        )

        self.navigator = navigator
        self.formatter = formatter
        self.hidden_roles_service = hidden_roles_service
        self.cleanup_service = cleanup_service

    async def on_click(self, interaction: discord.Interaction) -> None:
        flow = HiddenRolesFlow(
            navigator=self.navigator,
            formatter=self.formatter,
            hidden_roles_service=self.hidden_roles_service,
            cleanup_service=self.cleanup_service
        )

        await flow.start_for_add(
            interaction=interaction
        )


class DeleteHiddenRoleButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            formatter: SettingsFormatter,
            hidden_roles_service: HiddenRolesService,
            cleanup_service: CleanUpService,
            buttons_protection: ButtonProtectionService
    ):
        super().__init__(
            label='🗑️Delete hidden roles',
            style=discord.ButtonStyle.red,
            service=buttons_protection
        )

        self.navigator = navigator
        self.formatter = formatter
        self.hidden_roles_service = hidden_roles_service
        self.cleanup_service = cleanup_service

    async def on_click(self, interaction: discord.Interaction) -> None:
        flow = HiddenRolesFlow(
            navigator=self.navigator,
            formatter=self.formatter,
            hidden_roles_service=self.hidden_roles_service,
            cleanup_service=self.cleanup_service
        )

        await flow.start_for_delete(
            interaction=interaction
        )


class HiddenRolesListButton(FirewallButton):
    scope = 'admin'

    def __init__(self, formatter: SettingsFormatter, buttons_protection: ButtonProtectionService):
        super().__init__(
            label='📄Hidden roles list',
            style=discord.ButtonStyle.blurple,
            service=buttons_protection
        )

        self.formatter = formatter

    async def on_click(self, interaction: discord.Interaction) -> None:
        embed = await self.formatter.format_current_hidden_roles(interaction)

        await interaction.response.edit_message(
            embed=embed
        )
