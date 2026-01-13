import discord
import os

from core.bot_container import BotContainer

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.dm_messages = True
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix='', intents=intents)


container = BotContainer()
container.bot.override(bot)

container.wire(modules=[
    'modules.management.button_manager',
    'modules.buttons.views.for_admins.admin_menu',
    'services'
])


@bot.event
async def setup_hook():
    await bot.load_extension('core.management_cog')
    await bot.tree.sync()


bot.run(TOKEN)
