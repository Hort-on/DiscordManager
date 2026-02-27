from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from discord import app_commands
from discord.ext import commands

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator


class ManagementCog(commands.Cog):
    def __init__(self, navigator: Navigator):
        self.navigator = navigator

    @app_commands.command(
        name='mg',
        description='Opens bot menu.'
    )
    async def management(self, interaction: discord.Interaction):
        view = self.navigator.main_menu(
            guild_id=interaction.guild_id,
            user_id=interaction.user.id,
            owner_id=interaction.guild.owner_id
        )

        await interaction.response.send_message(
            view=view,
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(
        ManagementCog(navigator=bot.navigator)
    )
