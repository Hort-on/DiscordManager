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

load_dotenv()
TOKEN = os.getenv('TOKEN')


async def main():
    logger = Logger()

    db_connect = DB(logger=logger)
    db_factory = DBFactory(db_connect=db_connect, logger=logger)

    settings = SettingsStorage(bot=bot, db_factory=db_factory)

    birthday_manager = BirthdayManager(bot=bot, settings=settings, db_factory=db_factory)

    bad_words_handler = BadWordsHandler()

    member_left_notify = MemberLeftNotification(bot=bot, settings=settings)

    anti_bot_service = AntiBotService(settings=settings)

    navigator = Navigator()

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
        navigator=navigator
    )

    navigator.container = container

    BotController(bot=bot, settings=settings, db_factory=db_factory)

    AppContainer.set(container)

    await bot.load_extension('cogs.management_cog')
    await bot.start(TOKEN)

print("BOT ID:", id(bot))
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
