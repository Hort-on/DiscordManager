import discord
from discord.ui import View


class YesNoView(View):
    """View з кнопками Так/Ні"""

    def __init__(self, parent, config_key: str = None, on_decline_callback=None):
        super().__init__(timeout=60)
        self.parent = parent
        self.key = config_key
        self.on_decline_callback = on_decline_callback

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)

        if self.key:
            self.parent.config[self.key] = True

        await self.parent.next_step(interaction)

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)

        if self.key:
            self.parent.config[self.key] = False

        if self.on_decline_callback:
            await self.on_decline_callback(interaction)

        await self.parent.next_step(interaction)
