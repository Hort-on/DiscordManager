from __future__ import annotations

from typing import TYPE_CHECKING

import discord.ui

from features.auto_moderation.verification.buttons import AgreeButton, DisagreeButton

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.settings_storage.settings import SettingsStorage
    from ui.yes_no_service.yes_no_factory import YesNoViewFactory
    from features.auto_moderation.verification.service import VerificationService


class VerificationView(discord.ui.View):
    def __init__(
            self,
            bot: Bot,
            settings: SettingsStorage,
            yes_no_factory: YesNoViewFactory,
            service: VerificationService
    ):
        super().__init__(timeout=None)

        self.add_item(AgreeButton(
            bot=bot,
            settings=settings,
            yes_no_factory=yes_no_factory,
            service=service
        ))
        self.add_item(DisagreeButton(
            bot=bot,
            settings=settings,
            yes_no_factory=yes_no_factory,
            service=service
        ))
