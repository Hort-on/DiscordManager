from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator_context import NavigationContext

from features.for_admins.edit_settings.flows.sys_channels import SystemChannelsFlow

from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator import Navigator
    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter
    from features.for_admins.edit_settings.services.system_channels import SystemChannelsService


class SystemChannelsMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='System channels management',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        view = self.navigator.go(target='system_channels_menu')

        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='settings_menu')

        view.context = context

        await interaction.response.edit_message(view=view)


class AddSystemChannelsButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            sys_channels_service: SystemChannelsService,
            formatter: SettingsFormatter
    ):
        super().__init__(
            label='📥Add\\Change channels',
            style=discord.ButtonStyle.green
        )
        self.navigator = navigator
        self.service = sys_channels_service
        self.formatter = formatter

    async def on_click(self, interaction: discord.Interaction) -> None:
        flow = SystemChannelsFlow(
            navigator=self.navigator,
            sys_channels_service=self.service,
            formatter=self.formatter
        )

        await flow.start_for_add(
            interaction=interaction
        )


class DeleteSystemChannelsButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            sys_channels_service: SystemChannelsService,
            formatter: SettingsFormatter
    ):
        super().__init__(
            label='🗑️Delete system channels',
            style=discord.ButtonStyle.red
        )
        self.service = sys_channels_service
        self.navigator = navigator
        self.formatter = formatter

    async def on_click(self, interaction: discord.Interaction) -> None:
        flow = SystemChannelsFlow(
            navigator=self.navigator,
            sys_channels_service=self.service,
            formatter=self.formatter
        )

        await flow.start_for_delete(
            interaction=interaction,
        )


class SystemChannelsListButton(FirewallButton):
    scope = 'admin'

    def __init__(self, formatter: SettingsFormatter):
        super().__init__(
            label='📄System channels list',
            style=discord.ButtonStyle.blurple
        )
        self.formatter = formatter

    async def on_click(self, interaction: discord.Interaction) -> None:
        embed = await self.formatter.format_current_system_channels(guild=interaction.guild)

        await interaction.response.edit_message(embed=embed)
