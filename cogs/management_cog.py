import discord

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

from discord import app_commands
from discord.ext import commands

from modules.management.button_manager import ButtonManager

from services.utils.messages import GENERAL_MSGS as GM


class ManagementCog(commands.Cog):
    def __init__(
        self,
        settings: SettingsStorage
    ):
        self.settings = settings

    @app_commands.command(
        name="management",
        description="Opens management panel"
    )
    async def management(self, interaction: discord.Interaction):
        super_users_data = self.settings.set_storage.get_set(
            StorageTarget.SUPERUSERS,
            interaction.guild_id
        )

        if not super_users_data:
            await interaction.response.send_message(
                GM.get('superusers_not_found_msg'),
                ephemeral=True
            )
            return

        super_users = [user.get('user_id') for user in super_users_data]
        if interaction.user.id not in super_users:
            await interaction.response.send_message(
                GM.get('not_superuser_msg'),
                ephemeral=True
            )
            return

        view = ButtonManager(
            guild_id=interaction.guild_id,
        )

        await interaction.response.send_message(
            GM.get('ask_action_msg'),
            view=view,
            ephemeral=True
        )


async def setup(bot):
    settings = bot.controller.settings
    await bot.add_cog(ManagementCog(settings))
