import discord

from discord.ui import View


class YesNoView(View):
    def __init__(self, scenario):
        super().__init__(timeout=60)
        self.scenario = scenario

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True

        await interaction.edit_original_response(view=self)
        await self.scenario.yes_no_proceed(interaction, value=True)

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True

        await interaction.edit_original_response(view=self)
        await self.scenario.yes_no_proceed(interaction, value=False)
