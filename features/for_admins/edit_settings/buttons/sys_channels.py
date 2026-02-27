from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.routes import Route
from core.navigator.navigator_context import NavigationContext

from features.for_admins.edit_settings.flows.sys_channels import SystemChannelsFlow

from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter
    from features.for_admins.edit_settings.services.system_channels import SystemChannelsService
    from ui.button_protection.button_protection_service import ButtonProtectionService


class SystemChannelsMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            buttons_protection: ButtonProtectionService,
            formatter: SettingsFormatter,
            service: SystemChannelsService
    ):
        super().__init__(
            label='System channels management',
            style=discord.ButtonStyle.secondary,
            service=buttons_protection
        )

        self.navigator = navigator
        self.service = service
        self.formatter = formatter

    async def on_click(self, interaction: discord.Interaction) -> None:
        view = self.navigator.system_channels_menu()

        context = getattr(view, 'context', None)
        if context is None:
            context = NavigationContext()
            view.context = context

        context.push(target=Route.SETTINGS_MENU)

        await interaction.response.edit_message(view=view)


class AddSystemChannelsButton(FirewallButton):
    scope = 'admin'

    def __init__(self, buttons_protection: ButtonProtectionService, flow: SystemChannelsFlow):
        super().__init__(
            label='📥Add\\Change channels',
            style=discord.ButtonStyle.green,
            service=buttons_protection
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.start_for_add(interaction=interaction)


class DeleteSystemChannelsButton(FirewallButton):
    scope = 'admin'

    def __init__(self, buttons_protection: ButtonProtectionService, flow: SystemChannelsFlow):
        super().__init__(
            label='🗑️Delete system channels',
            style=discord.ButtonStyle.red,
            service=buttons_protection
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.start_for_delete(interaction=interaction)


class SystemChannelsListButton(FirewallButton):
    scope = 'admin'

    def __init__(self, buttons_protection: ButtonProtectionService, flow: SystemChannelsFlow):
        super().__init__(
            label='📄System channels list',
            style=discord.ButtonStyle.blurple,
            service=buttons_protection
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.for_sys_channels_list(interaction=interaction)
