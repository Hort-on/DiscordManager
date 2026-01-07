import discord


class StartView(discord.ui.View):
    @discord.ui.button(
        label="🎲 Randomizer",
        style=discord.ButtonStyle.primary
    )
    async def randomizer(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            content="Choose randomizer mode:",
            view=RandomizerModeView(),
            ephemeral=True
        )

