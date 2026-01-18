from dependency_injector import containers, providers

from database.data_base_model import DB
from database.settings_storage.settings import SettingsStorage

from modules.birthdays.birthday_repo import BirthdayManager
from modules.buttons.views.for_admins.admin_menu import AdminMenuView
from modules.logger.logger import Logger
from modules.management.button_manager import ButtonManager
from modules.management.events.member_left import MemberLeftNotification
from modules.management.message_handler.bad_words_handler import BadWordsHandler
from services.buttons.for_admins.superusers.add_superuser_service import AddSuperusersService

from services.buttons.for_admins.superusers.delete_superuser_service import DeleteSuperuserService
from services.factories.db_factory.db_scenario_factory import DBFactory
from services.other_services.get_channel import ChannelSelectorManager


class BotContainer(containers.DeclarativeContainer):
    # ========== primary init ==========
    bot = providers.Dependency()

    logger = providers.Singleton(Logger)

    db = providers.Singleton(
        DB,
        logger=logger,
    )

    db_factory = providers.Singleton(
        DBFactory,
        db_connect=db,
        logger=logger,
    )

    settings = providers.Singleton(
        SettingsStorage,
        bot=bot,
        db_factory=db_factory,
        logger=logger,
    )

    birthday_manager = providers.Singleton(
        BirthdayManager,
        db_factory=db_factory,
        logger=logger,
    )

    bad_words_handler = providers.Singleton(
        BadWordsHandler,
        logger=logger,
    )

    # ========== services init ==========
    member_left_notification = providers.Singleton(
        MemberLeftNotification,
        bot=bot,
        settings=settings,
        logger=logger,
    )

    delete_superuser_service = providers.Singleton(
        DeleteSuperuserService,
        settings=settings,
        db_factory=db_factory,
    )

    ch_selector_manager = providers.Singleton(
        ChannelSelectorManager,
        settings=settings
    )

    admin_menu_view = providers.Singleton(
        AdminMenuView,
        settings=settings,
        db_factory=db_factory,
        birthday=birthday_manager
    )

    add_superusers_service = providers.Singleton(
        AddSuperusersService,
        settings=settings,
        db_factory=db_factory
    )

    button_manager = providers.Singleton(
        ButtonManager,
        settings=settings
    )
