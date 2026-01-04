import discord


class RandomizeButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Randomize teams',
            style=discord.ButtonStyle.blurple
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()
