import discord

from services.embed_constructor.base import BaseEmbed


class ErrorEmbed(BaseEmbed):
    def __init__(self, description: str):
        super().__init__(
            title='❌ Error',
            description=description,
            color=discord.Color.red()
        )
