import discord


class BackButton(discord.ui.Button):
    def __init__(self, view_factory):
        super().__init__(
            label='↩️ Back',
            style=discord.ButtonStyle.secondary
        )
        self.view_factory = view_factory

    async def callback(self, interaction: discord.Interaction):
        self.view.disable_all_items()

        await interaction.edit_original_response(
            view=self.view_factory()
        )
