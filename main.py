from pathlib import Path
import os
import asyncio
import logging

from dotenv import load_dotenv

from core.bot_config import create_bot
from core.controller import Controller
from core.general_services_container import GeneralContainer
from core.navigator.navigator import Navigator

from database.data_base_model import DB
from database.settings_storage.settings import SettingsStorage
from database.db_factory.db_scenario_factory import DBFactory
from features.auto_moderation.message_moderation.module import build_automod_module

from features.auto_moderation.verification.view_service import VerificationViewService
from features.auto_moderation.verification.service import VerificationService
from features.for_admins.module import build_admin_module
from features.for_admins.send_messages.services.send_rules_service import RulesService
from features.for_everyone.module import build_everyone_module
# from features.for_everyone.birthdays.birthday_manager import BirthdayManager

from general_services.logger.logger import Logger
from general_services.other_services.cleanup_service import CleanUpService

from ui.button_protection.button_protection_service import ButtonProtectionService


# Logging
logging.basicConfig(level=logging.WARNING)
logging.getLogger('discord.http').setLevel(logging.DEBUG)

load_dotenv()
TOKEN = os.getenv('TOKEN')

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'database' / 'DATA' / 'assistant_data.sqlite'


async def main():
    bot = create_bot()

    logger = Logger()

    db_connect = DB(logger=logger, path=DB_PATH)
    await db_connect.init_tables()

    db_factory = DBFactory(db_connect=db_connect, logger=logger)

    settings = SettingsStorage(bot=bot, db_factory=db_factory)

    button_protector = ButtonProtectionService(settings=settings)

    cleanup_service = CleanUpService(settings=settings, db_factory=db_factory)

    verification_service = VerificationService(bot=bot, settings=settings, db_factory=db_factory)

    verification_view_service = VerificationViewService(bot=bot, settings=settings, service=verification_service)

    rules_service = RulesService(bot=bot, settings=settings)

    admin_module = build_admin_module(
        bot=bot,
        db_factory=db_factory,
        settings=settings,
        cleanup_service=cleanup_service,
        verification_service=verification_service,
        verification_view_service=verification_view_service,
        rules_service=rules_service
    )

    everyone_module = build_everyone_module(
        bot=bot,
        settings=settings,
        db_factory=db_factory
    )

    automod_module = build_automod_module(
        settings=settings
    )

    general_container = GeneralContainer(
        logger=logger,
        db_connect=db_connect,
        db_factory=db_factory,
        settings=settings,
        cleanup_service=cleanup_service,
        button_protection=button_protector
    )

    navigator = Navigator(
        general_container=general_container,
        admin_module=admin_module,
        everyone_module=everyone_module
    )

    bot.navigator = navigator

    Controller(
        bot=bot,
        navigator=navigator,
        settings=settings,
        db_factory=db_factory,
        verification_service=verification_service,
        verification_view_service=verification_view_service,
        rules_service=rules_service,
        moderation_service=automod_module
    )

    await bot.start(TOKEN)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
