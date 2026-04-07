from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.for_admins.delete_message.flow import DeleteMessageFlow
from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from features.for_admins.delete_message.service import DeleteMessageService
    from general_services.translator.translator import Translator
    from ui.button_protection.button_protection_service import ButtonProtectionService


class DeleteMessageButton(FirewallButton):
    scope = "admin"

    def __init__(
        self,
        guild_id: int,
        navigator: Navigator,
        context: NavigationContext,
        delete_msg_service: DeleteMessageService,
        buttons_protection: ButtonProtectionService,
        translator: Translator,
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id, section="DELETE_MESSAGES", key="delete_msg_title"
            ),
            style=discord.ButtonStyle.secondary,
            protection_service=buttons_protection,
        )

        self.navigator = navigator
        self.context = context
        self.service = delete_msg_service
        self.translator = translator

    async def on_click(self, interaction: discord.Interaction) -> None:
        flow = DeleteMessageFlow(
            delete_msg_service=self.service,
            navigator=self.navigator,
            context=self.context,
            translator=self.translator,
        )

        await flow.delete_message_start(interaction=interaction)
