from pathlib import Path

import os
import asyncio
from dotenv import load_dotenv

from core.bot_config import bot
from core.container import BotContainer, AppContainer
from core.controller import BotController

from database.data_base_model import DB
from database.settings_storage.settings import SettingsStorage

from modules.buttons.navigator import Navigator
from modules.management.birthdays.birthday_manager import BirthdayManager
from modules.management.events.member_left import MemberLeftNotification
from modules.management.message_handler.bad_words_handler import BadWordsHandler
from modules.management.verification.service import AntiBotService

from services.factories.db_factory.db_scenario_factory import DBFactory
from services.logger.logger import Logger
from services.yes_no_service.yes_no_factory import YesNoViewFactory

load_dotenv()
TOKEN = os.getenv('TOKEN')

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'database' / 'DATA' / 'assistant_data.sqlite'


async def main():
    logger = Logger()

    db_connect = DB(logger=logger, path=DB_PATH)
    await db_connect.init_tables()
    db_factory = DBFactory(db_connect=db_connect, logger=logger)

    settings = SettingsStorage(bot=bot, db_factory=db_factory)

    birthday_manager = BirthdayManager(bot=bot, settings=settings, db_factory=db_factory)

    bad_words_handler = BadWordsHandler()

    member_left_notify = MemberLeftNotification(bot=bot, settings=settings)

    navigator = Navigator()

    yes_no_factory = YesNoViewFactory()

    anti_bot_service = AntiBotService(settings=settings, yes_no_factory=yes_no_factory)

    container = BotContainer(
        bot=bot,
        db_connect=db_connect,
        db_factory=db_factory,
        logger=logger,
        settings=settings,
        birthday_manager=birthday_manager,
        bad_words_handler=bad_words_handler,
        member_left_notify=member_left_notify,
        anti_bot_service=anti_bot_service,
        navigator=navigator,
        yes_no_factory=yes_no_factory
    )

    navigator.container = container
    BotController(
        bot=bot,
        settings=settings,
        db_factory=db_factory,
        yes_no_factory=yes_no_factory
    )

    AppContainer.set(container)

    await bot.start(TOKEN)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
