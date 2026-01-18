import discord
import os

from discord.ext import commands

from dotenv import load_dotenv

from core.main import BotController
from database.data_base_model import DB
from database.settings_storage.settings import SettingsStorage
from modules.birthdays.birthday_repo import BirthdayManager

from modules.logger.logger import Logger
from modules.management.events.member_left import MemberLeftNotification
from modules.management.message_handler.bad_words_handler import BadWordsHandler
from services.factories.db_factory.db_scenario_factory import DBFactory

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

logger = Logger()

db_connect = DB(logger=logger)
db_factory = DBFactory(db_connect=db_connect, logger=logger)

settings = SettingsStorage(bot=bot, db_factory=db_factory)

birthday_manager = BirthdayManager(bot=bot, settings=settings, db_factory=db_factory)

bad_words_handler = BadWordsHandler()

member_left_notify = MemberLeftNotification(bot=bot, settings=settings)

bot.container = BotController(
    bot=bot,
    db_connect=db_connect,
    db_factory=db_factory,
    logger=logger,
    settings=settings,
    birthday_manager=birthday_manager,
    bad_words_handler=bad_words_handler,
    member_left_notify=member_left_notify
)


@bot.event
async def setup_hook():
    await bot.load_extension('core.management_cog')
    await bot.tree.sync()


bot.run(TOKEN)
