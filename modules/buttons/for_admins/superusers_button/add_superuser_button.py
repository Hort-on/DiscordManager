import discord.ui


class AddSUserButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Add super user',
            style = discord.ButtonStyle.green
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()

        await interaction.edit_original_response(
            content='',
            view=view,
        )
