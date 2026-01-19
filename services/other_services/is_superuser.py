from core.bot_container import AppContainer
from core.main import BotController

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget


class IsSuperuserService:
    def __init__(self):
        controller: BotController = AppContainer.get()

        self.settings: SettingsStorage = controller.settings

    def is_superuser(self, guild_id: int, user_id: int) -> bool:
        superusers = self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=guild_id
        )
        return user_id in superusers
