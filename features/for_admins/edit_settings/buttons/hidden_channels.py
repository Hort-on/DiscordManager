from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from ui.button_protection.admin_buttons_protection import FirewallButton

from features.for_admins.edit_settings.flows.hidden_channels import HiddenChannelsFlow


if TYPE_CHECKING:
    from core.navigator import Navigator

    from features.for_admins.edit_settings.services.hidden_channels import HiddenChannelsService
    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter

    from general_services.other_services.cleanup_service import CleanUpService

    from ui.button_protection.button_protection_service import ButtonProtectionService


class HiddenChannelsMenuButtons(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            buttons_protection: ButtonProtectionService,
            formatter: SettingsFormatter,
            hidden_ch_service: HiddenChannelsService,
            cleanup_service: CleanUpService
    ):
        super().__init__(
            label='Hidden channels management',
            style=discord.ButtonStyle.secondary,
            service=buttons_protection
        )

        self.hidden_ch_service = hidden_ch_service
        self.navigator = navigator
        self.formatter = formatter
        self.cleanup_service = cleanup_service

    async def on_click(self, interaction: discord.Interaction) -> None:
        flow = HiddenChannelsFlow(
            navigator=self.navigator,
            formatter=self.formatter,
            hidden_ch_service=self.hidden_ch_service,
            cleanup_service=self.cleanup_service
        )

        await flow.start_for_menu(interaction=interaction)


class AddHiddenChannelButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            hidden_ch_service: HiddenChannelsService,
            formatter: SettingsFormatter,
            cleanup_service: CleanUpService,
            buttons_protection: ButtonProtectionService
    ):
        super().__init__(
            label='📥Add hidden channels',
            style=discord.ButtonStyle.green,
            service=buttons_protection
        )

        self.hidden_ch_service = hidden_ch_service
        self.navigator = navigator
        self.formatter = formatter
        self.cleanup_service = cleanup_service

    async def on_click(self, interaction: discord.Interaction) -> None:
        flow = HiddenChannelsFlow(
            navigator=self.navigator,
            formatter=self.formatter,
            hidden_ch_service=self.hidden_ch_service,
            cleanup_service=self.cleanup_service
        )

        await flow.start_for_add(interaction=interaction)


class DeleteHiddenChannelButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            hidden_ch_service: HiddenChannelsService,
            formatter: SettingsFormatter,
            cleanup_service: CleanUpService,
            buttons_protection: ButtonProtectionService
    ):
        super().__init__(
            label='🗑️Delete hidden channels',
            style=discord.ButtonStyle.red,
            service=buttons_protection
        )

        self.hidden_ch_service = hidden_ch_service
        self.navigator = navigator
        self.formatter = formatter
        self.cleanup_service = cleanup_service

    async def on_click(self, interaction: discord.Interaction) -> None:
        flow = HiddenChannelsFlow(
            navigator=self.navigator,
            formatter=self.formatter,
            hidden_ch_service=self.hidden_ch_service,
            cleanup_service=self.cleanup_service
        )

        await flow.start_for_delete(interaction=interaction)


class HiddenChannelsListButton(FirewallButton):
    scope = 'admin'

    def __init__(self, formatter: SettingsFormatter, buttons_protection: ButtonProtectionService):
        super().__init__(
            label='📄Hidden channels list',
            style=discord.ButtonStyle.blurple,
            service=buttons_protection
        )

        self.formatter = formatter

    async def on_click(self, interaction: discord.Interaction) -> None:
        embed = await self.formatter.format_current_hidden_channels(interaction)

        await interaction.response.edit_message(embed=embed)
