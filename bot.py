import discord
import os

from core.main import BotController

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

GUILD_ID = int(os.getenv('GUILD_ID'))

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
controller = BotController()

bot.run(TOKEN)
