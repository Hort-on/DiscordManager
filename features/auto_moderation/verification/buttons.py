from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.auto_moderation.verification.flow import VerificationFlow
from features.auto_moderation.verification.service import VerificationService

from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from ui.yes_no_service.yes_no_factory import YesNoViewFactory
    from database.settings_storage.settings import SettingsStorage


class AgreeButton(FirewallButton):
    scope = 'user'

    def __init__(
            self,
            settings: SettingsStorage,
            yes_no_factory: YesNoViewFactory,
            service: VerificationService
    ):
        super().__init__(
            label='Agree',
            style=discord.ButtonStyle.green,
            custom_id='verify_agree'
        )

        self.settings = settings
        self.yes_no_factory = yes_no_factory
        self.service = service

    async def on_click(self, interaction: discord.Interaction) -> None:
        flow = VerificationFlow(
            settings=self.settings,
            yes_no_factory=self.yes_no_factory,
            service=self.service
        )

        await flow.agree_start(
            interaction=interaction
        )


class DisagreeButton(FirewallButton):
    scope = 'user'

    def __init__(
            self,
            settings: SettingsStorage,
            yes_no_factory: YesNoViewFactory,
            service: VerificationService
    ):
        super().__init__(
            label='Disagree',
            style=discord.ButtonStyle.red,
            custom_id='verify_disagree'
        )

        self.settings = settings
        self.yes_no_factory = yes_no_factory
        self.service = service

    async def on_click(self, interaction: discord.Interaction):
        flow = VerificationFlow(
            settings=self.settings,
            yes_no_factory=self.yes_no_factory,
            service=self.service
        )

        await flow.disagree_start(
            interaction=interaction
        )
