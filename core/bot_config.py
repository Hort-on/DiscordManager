import discord
from discord.ext import commands


class Bot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension('cogs.management_cog')

        guild = discord.Object(id=1017855127081717820)

        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)


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

    return Bot(intents=intents, command_prefix=None)


bot = create_bot()
