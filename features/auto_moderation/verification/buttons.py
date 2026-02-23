from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.auto_moderation.verification.flow import VerificationFlow
from features.auto_moderation.verification.service import VerificationService


if TYPE_CHECKING:
    from core.bot_config import Bot
    from ui.yes_no_service.yes_no_factory import YesNoViewFactory
    from database.settings_storage.settings import SettingsStorage


class AgreeButton(discord.ui.Button):
    def __init__(
            self,
            bot: Bot,
            settings: SettingsStorage,
            yes_no_factory: YesNoViewFactory,
            service: VerificationService
    ):
        super().__init__(
            label='Agree',
            style=discord.ButtonStyle.green,
            custom_id='verify_agree'
        )

        self.bot = bot
        self.settings = settings
        self.yes_no_factory = yes_no_factory
        self.service = service

    async def callback(self, interaction: discord.Interaction) -> None:
        flow = VerificationFlow(
            bot=self.bot,
            settings=self.settings,
            yes_no_factory=self.yes_no_factory,
            service=self.service
        )

        await flow.agreement_start(
            interaction=interaction
        )


class DisagreeButton(discord.ui.Button):
    def __init__(
            self,
            bot: Bot,
            settings: SettingsStorage,
            yes_no_factory: YesNoViewFactory,
            service: VerificationService
    ):
        super().__init__(
            label='Disagree',
            style=discord.ButtonStyle.red,
            custom_id='verify_disagree'
        )

        self.bot = bot
        self.settings = settings
        self.yes_no_factory = yes_no_factory
        self.service = service

    async def callback(self, interaction: discord.Interaction):
        flow = VerificationFlow(
            bot=self.bot,
            settings=self.settings,
            yes_no_factory=self.yes_no_factory,
            service=self.service
        )

        await flow.disagreement_start(
            interaction=interaction
        )
