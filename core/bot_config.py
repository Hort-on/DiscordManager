import discord
from discord.ext import commands


def create_bot():
    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True
    intents.presences = True
    intents.messages = True
    intents.dm_messages = True
    intents.message_content = True
    intents.moderation = True
    intents.typing = False

    return commands.Bot(command_prefix='', intents=intents)


bot = create_bot()
