from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from discord.ext import commands

    from database.data_base_model import DB
    from database.settings_storage.settings import SettingsStorage
    from core.navigator import Navigator

    from features.birthdays import BirthdayManager
    from features.moderation.message_handler import BadWordsHandler
    from modules.verification.service import AntiBotService

    from database.db_factory.db_scenario_factory import DBFactory
    from general_services.logger.logger import Logger
    from ui.yes_no_service import YesNoViewFactory


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
            anti_bot_service: AntiBotService,
            navigator: Navigator,
            yes_no_factory: YesNoViewFactory
    ):
        self.bot = bot
        self.db_connect = db_connect
        self.db_factory = db_factory
        self.logger = logger
        self.settings = settings
        self.birthday_manager = birthday_manager
        self.bad_words = bad_words_handler
        self.anti_bot_service = anti_bot_service
        self.navigator = navigator
        self.yes_no_factory = yes_no_factory


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
