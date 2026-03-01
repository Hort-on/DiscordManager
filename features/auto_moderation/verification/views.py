from __future__ import annotations

from typing import TYPE_CHECKING

import discord.ui

from features.auto_moderation.verification.buttons import AgreeButton, DisagreeButton

if TYPE_CHECKING:
    from features.auto_moderation.verification.flow import VerificationFlow


class VerificationView(discord.ui.View):
    def __init__(self, flow: VerificationFlow):
        super().__init__(timeout=None)

        self.add_item(AgreeButton(flow=flow))
        self.add_item(DisagreeButton(flow=flow))
