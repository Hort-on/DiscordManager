import discord

from services.embed_constructor.base import BaseEmbed


class SuccessEmbed(BaseEmbed):
    def __init__(self, description: str):
        super().__init__(
            title='✅ Success',
            description=description,
            color=discord.Color.green()
        )
