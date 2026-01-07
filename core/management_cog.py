import discord
from discord import app_commands
from discord.ext import commands

from database.settings_storage.settings_storage import SettingsStorage

from services.factories.db_factory.db_scenario_factory import DBScenarioFactory

from modules.birthdays.birthday_repo import BirthdayRepo
from modules.logger.logger import Logger
from modules.management.channels_processing.management import Management

from services.utils.messages import GENERAL_MSGS, CONFIG_MSGS


class ManagementCog(commands.Cog):
    def __init__(
            self,
            bot,
            settings: SettingsStorage,
            db: DBScenarioFactory,
            logger: Logger,
            birthday: BirthdayRepo
    ):

        self.bot = bot
        self.settings = settings
        self.db = db
        self.logger = logger
        self.birthday = birthday

    @app_commands.command(
        name="management",
        description="Open management panel"
    )
    async def management(self, interaction: discord.Interaction):
        super_users_data = self.settings.get_guild_superusers(interaction.guild_id)
        if not super_users_data:
            await interaction.response.send_message(
                GENERAL_MSGS.get('superusers_not_found_msg'),
                ephemeral=True
            )
            return

        super_users = [user.get('user_id') for user in super_users_data]
        if interaction.user.id not in super_users:
            await interaction.response.send_message(
                GENERAL_MSGS.get('not_superuser_msg'),
                ephemeral=True
            )
            return

        if not self.settings.get_guild_settings(interaction.guild_id).get('configuration_done'):
            await interaction.response.send_message(
                CONFIG_MSGS.get('no_configuration_msg'),
                ephemeral=True
            )
            return

        view = Management(interaction.guild_id, self.settings, self.db, self.birthday, self.logger)
        await interaction.response.send_message(
            GENERAL_MSGS.get('ask_action_msg'),
            view=view,
            ephemeral=True
        )


async def setup(bot):
    services = bot.services
    await bot.add_cog(
        ManagementCog(
            bot,
            services.guilds_settings,
            services.db,
            services.logger,
            services.birthday
        )
    )
