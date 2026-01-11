import discord

from services.modals.random_modal.numberl import RandomNumModal


class RandomNumButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Random number',
            style=discord.ButtonStyle.secondary
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.send_modal(RandomNumModal())
