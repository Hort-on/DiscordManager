import discord

from services.embed_constructor.base import BaseEmbed


class InfoEmbed(BaseEmbed):
    def __init__(self, description: str):
        super().__init__(
            title='ℹ️ Info',
            description=description,
            color=discord.Color.blurple()
        )
