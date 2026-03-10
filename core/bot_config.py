import discord
from discord.ext import commands


class Bot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension('cogs.management_cog')
        await self.tree.sync()


def create_bot():
    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True
    intents.messages = True
    intents.dm_messages = True
    intents.message_content = True
    intents.moderation = True
    intents.typing = False

    return Bot(intents=intents, command_prefix='!')


bot = create_bot()
