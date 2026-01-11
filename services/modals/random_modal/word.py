import discord

from services.button_services.randomizer_service.words import RandomWordService


class RandomWordModal(discord.ui.Modal, title='Random word'):
    def __init__(self):
        super().__init__()
        self.random_proceed = RandomWordService()

    words = discord.ui.TextInput(
        label='Words',
        placeholder='Please enter words separated by coma',
        required=True,
        max_length=3
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.random_proceed.random_word_proceed(
            interaction,
            str(self.words.value)
        )
