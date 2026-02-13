from __future__ import annotations

from typing import TYPE_CHECKING

from ui.yes_no_service.yes_no_factory import YesNoViewFactory

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage

import discord

from modules.verification.service import AgreeButtonService


class AntiBotModal(discord.ui.Modal, title='Anti-bot check'):
    def __init__(
            self,
            settings: SettingsStorage,
            yes_no_factory: YesNoViewFactory
    ):
        super().__init__()
        self.anti_bot_check = AgreeButtonService(
            settings=settings,
            yes_no_factory=yes_no_factory
        )

    check_word = discord.ui.TextInput(
        label='Please write the word "Hello"',
        placeholder='write here',
        required=True,
        max_length=5,
        min_length=5
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.anti_bot_check.check_the_word(interaction=interaction, word=self.check_word.value)
