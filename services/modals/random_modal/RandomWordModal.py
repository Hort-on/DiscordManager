import discord


class RandomWordModal(discord.ui.Modal, title='Random word'):
    def __init__(self):
        super().__init__()

    word_list = discord.ui.TextInput(
        label='Words',
        placeholder='Please enter words separated by coma',
        required=True,
        max_length=3
    )

    async def on_submit(self, interaction: discord.Interaction) -> None: