from dependency_injector.wiring import Provide, inject

from core.bot_container import BotContainer
from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget


class IsSuperuserService:
    @inject
    def __init__(self, settings: SettingsStorage = Provide[BotContainer.settings]):
        self.settings = settings

    def is_superuser(self, guild_id: int, user_id: int) -> bool:
        superusers = self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=guild_id
        )
        return user_id in superusers
