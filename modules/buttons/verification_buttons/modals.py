import discord

from modules.buttons.verification_buttons.service import AntiBotService


class AgreeModal(discord.ui.Modal, title='Anti-bot check'):
    def __init__(self):
        super().__init__()
        self.anti_bot_check = AntiBotService()

    check_word = discord.ui.TextInput(
        label='Please write the word "Hello"',
        placeholder='write here',
        required=True,
        max_length=5,
        min_length=5
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.anti_bot_check.check_the_word(interaction=interaction, word=self.check_word.value)
