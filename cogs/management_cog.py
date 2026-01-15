import discord

from discord import app_commands
from discord.ext import commands

from modules.management.button_manager import ButtonManager

from services.utils.messages import GENERAL_MSGS as GM


class ManagementCog(commands.Cog):
    @app_commands.command(
        name="management",
        description="Opens management panel"
    )
    async def management(self, interaction: discord.Interaction):
        view = ButtonManager(
            guild_id=interaction.guild_id,
            user_id=interaction.user.id
        )

        await interaction.response.send_message(
            GM.get('ask_action_msg'),
            view=view,
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(ManagementCog())
