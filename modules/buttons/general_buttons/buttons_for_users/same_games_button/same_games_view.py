import discord


# TODO: оепепнахрх же ме рю ймнойю
class SameGameButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Show members with the same game roles",
            style=discord.ButtonStyle.blurple
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()
