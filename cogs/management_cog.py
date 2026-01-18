import discord

from discord import app_commands
from discord.ext import commands

from database.settings_storage.settings import SettingsStorage

from modules.birthdays.birthday_repo import BirthdayManager
from modules.management.button_manager import ButtonManager

from services.factories.db_factory.db_scenario_factory import DBFactory
from services.utils.messages import GENERAL_MSGS as GM


class ManagementCog(commands.Cog):
    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBFactory,
            birthday_manager: BirthdayManager
    ):
        self.settings = settings
        self.db_factory = db_factory
        self.birthday_manager = birthday_manager

    @app_commands.command(
        name="management",
        description="Opens management panel"
    )
    async def management(self, interaction: discord.Interaction):
        view = ButtonManager(
            settings=self.settings,
            db_factory=self.db_factory,
            birthday_manager=self.birthday_manager,
            guild_id=interaction.guild_id,
            user_id=interaction.user.id,
        )

        await interaction.response.send_message(
            GM.get('ask_action_msg'),
            view=view,
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(ManagementCog(
        settings=bot.container.settings,
        db_factory=bot.container.db_factory,
        birthday_manager=bot.container.birthday_manager
    ))
