from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from discord.ext import commands

    from database.data_base_model import DB
    from database.settings_storage.settings import SettingsStorage
    from modules.buttons.navigator import Navigator

    from modules.management.birthdays.birthday_manager import BirthdayManager
    from modules.management.events.member_left import MemberLeftNotification
    from modules.management.message_handler.bad_words_handler import BadWordsHandler
    from modules.management.verification.service import AntiBotService

    from services.factories.db_factory.db_scenario_factory import DBFactory
    from services.logger.logger import Logger


class BotContainer:
    def __init__(
            self,
            bot: commands.Bot,
            db_connect: DB,
            db_factory: DBFactory,
            logger: Logger,
            settings: SettingsStorage,
            birthday_manager: BirthdayManager,
            bad_words_handler: BadWordsHandler,
            member_left_notify: MemberLeftNotification,
            anti_bot_service: AntiBotService,
            navigator: Navigator
    ):
        self.bot = bot
        self.db_connect = db_connect
        self.db_factory = db_factory
        self.logger = logger
        self.settings = settings
        self.birthday_manager = birthday_manager
        self.bad_words = bad_words_handler
        self.member_left_notify = member_left_notify
        self.anti_bot_service = anti_bot_service
        self.navigator = navigator


class AppContainer:
    _instance: BotContainer | None = None

    @classmethod
    def set(cls, container: BotContainer):
        cls._instance = container

    @classmethod
    def get(cls) -> BotContainer:
        if cls._instance is None:
            raise RuntimeError('Container not initialized')
        return cls._instance
