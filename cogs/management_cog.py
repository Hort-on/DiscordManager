from __future__ import annotations

import discord

from discord import app_commands
from discord.ext import commands

from core.container import AppContainer

from modules.buttons.navigator import Navigator

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.container import BotContainer


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
    container: BotContainer = AppContainer.get()
    await bot.add_cog(
        ManagementCog(
            navigator=container.navigator
        )
    )
