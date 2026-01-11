import discord

from services.button_services.randomizer_service.numbers import RandomNumService


class RandomNumModal(discord.ui.Modal, title='Random number'):
    def __init__(self):
        super().__init__()
        self.random_proceed = RandomNumService()

    first_num = discord.ui.TextInput(
        label='First number',
        placeholder='Please enter the first number min 0',
        required=True,
        max_length=3
    )

    second_num = discord.ui.TextInput(
        label='Second number',
        placeholder='Please enter a number min 1',
        required=True,
        max_length=3
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.random_proceed.random_num_proceed(
            interaction,
            int(self.first_num.value),
            int(self.second_num.value)
        )
