import discord
from discord import app_commands
from discord.ext import commands

from modules.configuration.starting_configuration import ConfigurationView
from database.data_base_model import DB


class StartCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DB()

    @app_commands.command(
        name="start",
        description="Start server configuration"
    )
    async def start_config(self, interaction: discord.Interaction):
        config_done = await self.db.get_data(
            interaction.guild.id,
            'settings',
            'configuration_done'
        )

        if config_done:
            await interaction.response.send_message(
                "You have already configured the bot for this server.",
                ephemeral=True
            )
            return

        view = ConfigurationView()
        await interaction.response.send_message(
            "Welcome to the configuration!",
            view=view,
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(StartCog(bot))
