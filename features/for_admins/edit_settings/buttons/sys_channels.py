from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.params_containers import GeneralParams
from core.navigator.routes import Route

from features.for_admins.edit_settings.flows.sys_channels import SystemChannelsFlow

from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter
    from ui.button_protection.button_protection_service import ButtonProtectionService
    from general_services.translator.translator import Translator


class SystemChannelsMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            context: NavigationContext,
            buttons_protection: ButtonProtectionService,
            formatter: SettingsFormatter,
            translator: Translator,
            guild_id: int
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='EDIT_SETTINGS',
                key='sys_ch_menu'
            ),
            style=discord.ButtonStyle.secondary,
            protection_service=buttons_protection
        )

        self.navigator = navigator
        self.context = context
        self.formatter = formatter

    async def on_click(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        assert guild is not None

        view = self.navigator.system_channels_menu(context=self.context, guild_id=guild.id)
        view.context = self.context

        self.context.push(
            target=Route.SETTINGS_MENU,
            params=GeneralParams(guild_id=guild.id)
        )

        await interaction.response.edit_message(view=view)


class AddSystemChannelsButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            buttons_protection: ButtonProtectionService,
            flow: SystemChannelsFlow,
            translator: Translator,
            guild_id: int
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='EDIT_SETTINGS',
                key='add_sys_ch'
            ),
            style=discord.ButtonStyle.green,
            protection_service=buttons_protection
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.start_for_add(interaction=interaction)


class DeleteSystemChannelsButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            buttons_protection: ButtonProtectionService,
            flow: SystemChannelsFlow,
            translator: Translator,
            guild_id: int
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='EDIT_SETTINGS',
                key='delete_sys_ch'
            ),
            style=discord.ButtonStyle.red,
            protection_service=buttons_protection
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.start_for_delete(interaction=interaction)


class SystemChannelsListButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            buttons_protection: ButtonProtectionService,
            flow: SystemChannelsFlow,
            translator: Translator,
            guild_id: int
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='EDIT_SETTINGS',
                key='add_hidden_roles'
            ),
            style=discord.ButtonStyle.blurple,
            protection_service=buttons_protection
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.for_sys_channels_list(interaction=interaction)
