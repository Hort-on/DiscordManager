import discord

from discord import app_commands
from discord.ext import commands

from modules.buttons.navigator import Navigator


class ManagementCog(commands.Cog):
    def __init__(self, navigator: Navigator):
        self.navigator = navigator

    @app_commands.command(
        name='management',
        description='Opens management panel'
    )
    async def management(self, interaction: discord.Interaction):
        await self.navigator.go(
            target='main_menu',
            interaction=interaction,
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(
        ManagementCog(
            navigator=bot.navigator
        )
    )

