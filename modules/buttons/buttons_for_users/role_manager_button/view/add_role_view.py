import discord


class AddRoleButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Add role',
            style=discord.ButtonStyle.blurple
        )

    def callback(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()
        await interaction.response