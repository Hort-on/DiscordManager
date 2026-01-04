import discord
import os

from core.main import BotController

from discord.ext import commands
from dotenv import load_dotenv

from database.data_base_model import DB
from factories.db_factory import DBScenarioFactory
from database.settings_storage.settings_storage import SettingsStorage

from modules.birthdays.birthday_repo import BirthdayRepo
from modules.logger.logger import Logger
from modules.management.events_processing.member_left_event import MemberLeftNotification
from modules.management.message_processing.BadWordsHandler import BadWordsHandler

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='', intents=discord.Intents.all())

# --------------------------- DEPENDENCIES --------------------------- #
logger = Logger()

db_connect = DB(logger)
db_factory = DBScenarioFactory(db_connect=db_connect, logger=logger)

guild_settings = SettingsStorage(bot, db_factory)

birthday_repo = BirthdayRepo(bot, guild_settings, db_factory)

bad_words_handler = BadWordsHandler()

member_left_notify = MemberLeftNotification(bot, guild_settings)

controller = BotController(
    bot,
    db_connect,
    db_factory,
    logger,
    guild_settings,
    birthday_repo,
    bad_words_handler,
    member_left_notify
)

bot.services = controller


# --------------------------- COGS --------------------------- #
@bot.event
async def setup_hook():
    await bot.load_extension('core.management_cog')
    await bot.tree.sync()


bot.run(TOKEN)
