import discord

from discord.ui import View


class YesNoView(View):
    def __init__(self, scenario):
        super().__init__(timeout=60)
        self.scenario = scenario

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def yes_button(self, interaction, _):
        await self.scenario.yes_no_proceed(
            interaction=interaction,
            value=True
        )

    @discord.ui.button(label='No', style=discord.ButtonStyle.red)
    async def no_button(self, interaction, _):
        await self.scenario.yes_no_proceed(
            interaction=interaction,
            value=False
        )
