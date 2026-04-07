from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.for_admins.send_messages.buttons import SendMessageButton, SendRulesButton
from features.for_admins.send_messages.flows.send_rules_flow import SendRulesFlow
from ui.buttons.back_button import BackButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_admins.send_messages.flows.send_message_flow import (
        SendMessageFlow,
    )
    from general_services.translator.translator import Translator
    from ui.button_protection.button_protection_service import ButtonProtectionService


class SendMessageMenuView(discord.ui.View):
    def __init__(
        self,
        navigator: Navigator,
        buttons_protection: ButtonProtectionService,
        messages_flow: SendMessageFlow,
        rules_flow: SendRulesFlow,
        translator: Translator,
        guild_id: int,
    ):
        super().__init__(timeout=60)

        self.add_item(
            SendMessageButton(
                protection_service=buttons_protection,
                flow=messages_flow,
                translator=translator,
                guild_id=guild_id,
            )
        )

        self.add_item(
            SendRulesButton(
                protection_service=buttons_protection,
                flow=rules_flow,
                translator=translator,
                guild_id=guild_id,
            )
        )

        self.add_item(
            BackButton(navigator=navigator, translator=translator, guild_id=guild_id)
        )
