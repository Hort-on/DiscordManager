from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.params_containers import GeneralParams
from core.navigator.routes import Route

from ui.button_protection.admin_buttons_protection import FirewallButton

from features.for_admins.edit_settings.flows.hidden_channels import HiddenChannelsFlow

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext

    from features.for_admins.edit_settings.services.hidden_channels import HiddenChannelsService
    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter

    from general_services.other_services.cleanup_service import CleanUpService
    from general_services.translator.translator import Translator

    from ui.button_protection.button_protection_service import ButtonProtectionService


class HiddenChannelsMenuButtons(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            context: NavigationContext,
            buttons_protection: ButtonProtectionService,
            formatter: SettingsFormatter,
            hidden_ch_service: HiddenChannelsService,
            cleanup_service: CleanUpService,
            translator: Translator,
            guild_id: int
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='EDIT_SETTINGS',
                key='hidden_ch_menu'
            ),
            style=discord.ButtonStyle.secondary,
            protection_service=buttons_protection
        )

        self.navigator = navigator
        self.context = context
        self.hidden_ch_service = hidden_ch_service
        self.formatter = formatter
        self.cleanup_service = cleanup_service

    async def on_click(self, interaction: discord.Interaction) -> None:
        view = self.navigator.hidden_channels_menu(
            context=self.context,
            guild_id=interaction.guild_id
        )

        view.context = self.context
        self.context.push(
            target=Route.SETTINGS_MENU,
            params=GeneralParams(
                guild_id=interaction.guild_id
            )
        )

        await interaction.response.edit_message(view=view)


class AddHiddenChannelButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            buttons_protection: ButtonProtectionService,
            flow: HiddenChannelsFlow,
            translator: Translator,
            guild_id: int
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='EDIT_SETTINGS',
                key='add_hidden_ch'
            ),
            style=discord.ButtonStyle.green,
            protection_service=buttons_protection
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.start_for_add(interaction=interaction)


class DeleteHiddenChannelButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            buttons_protection: ButtonProtectionService,
            flow: HiddenChannelsFlow,
            translator: Translator,
            guild_id: int
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='EDIT_SETTINGS',
                key='delete_hidden_ch'
            ),
            style=discord.ButtonStyle.red,
            protection_service=buttons_protection
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.start_for_delete(interaction=interaction)


class HiddenChannelsListButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            buttons_protection: ButtonProtectionService,
            flow: HiddenChannelsFlow,
            translator: Translator,
            guild_id: int
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='EDIT_SETTINGS',
                key='hidden_ch_list'
            ),
            style=discord.ButtonStyle.blurple,
            protection_service=buttons_protection
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.for_channels_list(interaction=interaction)
