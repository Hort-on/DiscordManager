from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage
    from ui.yes_no_service.yes_no_factory import YesNoViewFactory

import discord.ui

from features.verification.buttons import AgreeButton, DisagreeButton


class VerificationView(discord.ui.View):
    def __init__(
            self,
            settings: SettingsStorage,
            yes_no_factory: YesNoViewFactory
    ):
        super().__init__(timeout=None)

        self.add_item(AgreeButton(
            settings=settings,
            yes_no_factory=yes_no_factory
        ))
        self.add_item(DisagreeButton())
