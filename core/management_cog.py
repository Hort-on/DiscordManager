import discord
from discord import app_commands
from discord.ext import commands

from modules.Management.channels_processing.management import Management
from database.data_base_model import DB


class ManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DB()

    @app_commands.command(
        name="management",
        description="Open management panel"
    )
    async def management(self, interaction: discord.Interaction):

        super_users_data = await self.db.get_data(
            interaction.guild.id,
            'super_users',
            'user_id'
        )

        if not super_users_data:
            await interaction.response.send_message(
                "Super users are not configured for this server.",
                ephemeral=True
            )
            return

        super_users = [user.get('user_id') for user in super_users_data]

        if interaction.user.id not in super_users:
            await interaction.response.send_message(
                "You do not have permission to use this feature!",
                ephemeral=True
            )
            return

        settings = await self.db.get_data(
            interaction.guild.id,
            "settings",
            'birthday',
            'sending_messages',
            'deleting_message',
            'congrats_channel_id',
            'system_channel_id',
            'verification_channel_id',
            'configuration_done'
        )

        if not settings.get("configuration_done"):
            await interaction.response.send_message(
                "Settings are not configured yet!",
                ephemeral=True
            )
            return

        view = Management(interaction, self.bot, settings)
        await interaction.response.send_message(
            "Select an action:",
            view=view,
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(ManagementCog(bot))