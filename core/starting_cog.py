import discord
from discord import app_commands
from discord.ext import commands

from database.db_factory.db_scenario_factory import DBScenarioFactory

from modules.configuration.starting_configuration import ConfigurationView
from modules.logger.logger import Logger

from utils.messages import CONFIG_MSGS


class StartCog(commands.Cog):
    def __init__(self, bot, db_factory: DBScenarioFactory, logger: Logger):
        self.bot = bot
        self.db_factory = db_factory
        self.logger = logger

    @app_commands.command(
        name="start",
        description="Start server configuration"
    )
    async def start_config(self, interaction: discord.Interaction):
        scenario_get_data = self.db_factory.for_get_data(
            interaction.guild.id,
            'settings',
            'configuration_done'
        )

        config_done = await scenario_get_data.db_proceed()

        if not config_done:
            return

        await interaction.response.send_message(
            CONFIG_MSGS.get('configuration_exists_msg'),
            ephemeral=True
        )

        view = ConfigurationView(self.db_factory)
        await interaction.response.send_message(
            CONFIG_MSGS.get('config_welcome_msg'),
            view=view,
            ephemeral=True
        )


async def setup(bot):
    services = bot.services
    await bot.add_cog(
        StartCog(
            bot,
            services.db,
            services.logger
        )
    )
