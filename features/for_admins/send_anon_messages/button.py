from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.for_admins.send_anon_messages.flow import SendAnonMsg

from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_admins.send_anon_messages.service import SendAnonMessageService
    from ui.button_protection.button_protection_service import ButtonProtectionService


class SendMessageButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            send_msg_service: SendAnonMessageService,
            buttons_protection: ButtonProtectionService
    ):
        super().__init__(
            label='Send message',
            style=discord.ButtonStyle.blurple,
            protection_service=buttons_protection
        )
        self.navigator = navigator
        self.service = send_msg_service

    async def on_click(self, interaction: discord.Interaction):
        flow = SendAnonMsg(
            send_msg_service=self.service,
            navigator=self.navigator
        )

        await flow.start_for_send(
            interaction=interaction
        )
