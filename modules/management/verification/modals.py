import discord

from core.container import AppContainer

from modules.management.verification.service import AntiBotService

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.controller import BotController


class AgreeModal(discord.ui.Modal, title='Anti-bot check'):
    def __init__(self):
        super().__init__()
        controller: 'BotController' = AppContainer.get()
        self.anti_bot_check = AntiBotService(controller.settings)

    check_word = discord.ui.TextInput(
        label='Please write the word "Hello"',
        placeholder='write here',
        required=True,
        max_length=5,
        min_length=5
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.anti_bot_check.check_the_word(interaction=interaction, word=self.check_word.value)
