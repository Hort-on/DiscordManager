from __future__ import annotations

from typing import TYPE_CHECKING

import discord.ui

from features.auto_moderation.verification.buttons import AgreeButton, DisagreeButton

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.settings_storage.settings import SettingsStorage
    from features.auto_moderation.verification.service import VerificationService
    from features.auto_moderation.verification.flow import VerificationFlow


class VerificationView(discord.ui.View):
    def __init__(
            self,
            flow: VerificationFlow,
            bot: Bot,
            settings: SettingsStorage,
            service: VerificationService
    ):
        super().__init__(timeout=None)

        self.add_item(AgreeButton(
            flow=flow,
            bot=bot,
            settings=settings,
            service=service
        ))
        self.add_item(DisagreeButton(
            flow=flow,
            bot=bot,
            settings=settings,
            service=service
        ))
