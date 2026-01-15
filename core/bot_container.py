from dependency_injector import containers, providers

from database.data_base_model import DB
from database.settings_storage.settings import SettingsStorage

from modules.birthdays.birthday_repo import BirthdayManager
from modules.logger.logger import Logger
from modules.management.events.member_left import MemberLeftNotification
from modules.management.message_handler.bad_words_handler import BadWordsHandler

from services.factories.db_factory.db_scenario_factory import DBScenarioFactory


class BotContainer(containers.DeclarativeContainer):

    # =====================
    # Core
    # =====================
    bot = providers.Dependency()

    logger = providers.Singleton(Logger)

    # =====================
    # Infrastructure
    # =====================
    db = providers.Singleton(
        DB,
        logger=logger,
    )

    db_factory = providers.Singleton(
        DBScenarioFactory,
        db_connect=db,
        logger=logger,
    )

    settings = providers.Singleton(
        SettingsStorage,
        bot=bot,
        db_factory=db_factory,
        logger=logger,
    )

    # =====================
    # Domain services
    # =====================
    birthday_manager = providers.Singleton(
        BirthdayManager,
        db_factory=db_factory,
        logger=logger,
    )

    bad_words_handler = providers.Singleton(
        BadWordsHandler,
        logger=logger,
    )

    member_left_notification = providers.Singleton(
        MemberLeftNotification,
        bot=bot,
        settings=settings,
        logger=logger,
    )
