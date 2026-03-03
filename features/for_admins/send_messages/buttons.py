from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.params_containers import AdminMenuParams
from core.navigator.routes import Route

from features.for_admins.send_messages.flows.send_message_flow import SendMessageFlow

from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from features.for_admins.send_messages.flows.send_rules_flow import SendRulesFlow
    from ui.button_protection.button_protection_service import ButtonProtectionService


class SendMessageMenu(FirewallButton):
    def __init__(
            self,
            navigator: Navigator,
            context: NavigationContext,
            protection_service: ButtonProtectionService
    ):
        super().__init__(
            label='📨Send message',
            style=discord.ButtonStyle.secondary,
            protection_service=protection_service
        )

        self.navigator = navigator
        self.context = context

    async def on_click(self, interaction: discord.Interaction) -> None:
        view = self.navigator.send_message_menu()

        view.context = self.context
        self.context.push(
            target=Route.ADMIN_MENU,
            params=AdminMenuParams(
                guild_id=interaction.guild_id
            )
        )

        await interaction.response.edit_message(view=view)


class SendMessageButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            protection_service: ButtonProtectionService,
            flow: SendMessageFlow
    ):
        super().__init__(
            label='Send message',
            style=discord.ButtonStyle.blurple,
            protection_service=protection_service
        )
        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.start_for_send(interaction=interaction)


class SendRulesButton(FirewallButton):
    scope = 'admin'

    def __init__(self, protection_service: ButtonProtectionService, flow: SendRulesFlow):
        super().__init__(
            label='Send the rules',
            style=discord.ButtonStyle.secondary,
            protection_service=protection_service
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.start_for_rules(interaction=interaction)
