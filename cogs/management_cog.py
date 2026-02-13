from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.container import BotContainer
    from core.navigator import Navigator

import discord

from discord import app_commands
from discord.ext import commands

from core.container import AppContainer


class ManagementCog(commands.Cog):
    def __init__(self, navigator: Navigator):
        self.navigator = navigator

    @app_commands.command(
        name='mg',
        description='Opens management panel'
    )
    async def management(self, interaction: discord.Interaction):
        view = self.navigator.go(
            target='main_menu',
            guild=interaction.guild,
            user_id=interaction.user.id
        )

        await interaction.response.send_message(
            view=view,
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(
        ManagementCog(navigator=container.navigator)
    )
