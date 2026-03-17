from __future__ import annotations

from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from features.auto_moderation.verification.flow import VerificationFlow
    from general_services.translator.translator import Translator


class AntiBotModal(discord.ui.Modal, title='Anti-bot check'):
    def __init__(
            self,
            flow: VerificationFlow,
            translator: Translator,
            guild_id: int
    ):
        super().__init__(
            title=translator.t(
                guild_id=guild_id,
                section='VERIFICATION',
                key='anti_bot_title'
            )
        )
        self.flow = flow

        self.check_word = discord.ui.TextInput(
            label=translator.t(
                guild_id=guild_id,
                section='VERIFICATION',
                key='word_label'
            ),
            placeholder=translator.t(
                guild_id=guild_id,
                section='VERIFICATION',
                key='word_placeholder'
            ),
            required=True,
            max_length=5,
            min_length=5
        )

        self.add_item(self.check_word)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.flow.word_verification(interaction=interaction, word=self.check_word.value)
