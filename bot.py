import discord
import os

from core.main import BotController

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='', intents=discord.Intents.all())
@bot.event
async def setup_hook():
    await bot.load_extension('core.start_cog')
    await bot.load_extension('core.management_cog')
    await bot.tree.sync()

controller = BotController(bot)

bot.run(TOKEN)
