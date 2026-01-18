import discord

from services.embed_constructor.base import BaseEmbed


class WarningEmbed(BaseEmbed):
    def __init__(self, description: str):
        super().__init__(
            title='⚠️ Warning',
            description=description,
            color=discord.Color.gold()
        )
