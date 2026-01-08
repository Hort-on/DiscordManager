import discord


class RandomNumModal(discord.ui.Modal, title='Random number'):
    def __init__(self):
        super().__init__()

    first_number = discord.ui.TextInput(
        label='First number',
        placeholder='Please enter the first number min 0',
        required=True,
        max_length=3
    )

    second_number = discord.ui.TextInput(
        label='Second number',
        placeholder='Please enter a number min 1',
        required=True,
        max_length=3
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
