from __future__ import annotations

from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from features.auto_moderation.verification.flow import VerificationFlow


class AntiBotModal(discord.ui.Modal, title='Anti-bot check'):
    def __init__(
            self,
            flow: VerificationFlow
    ):
        super().__init__()
        self.flow = flow

    check_word = discord.ui.TextInput(
        label='Please write the word "Hello"',
        placeholder='write here',
        required=True,
        max_length=5,
        min_length=5
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.flow.word_verification(interaction=interaction, word=self.check_word.value)
