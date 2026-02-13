import discord

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget


class IsSuperuserService:
    def __init__(self, settings: SettingsStorage):
        self.settings = settings

    def is_superuser(self, guild: discord.Guild, user_id: int) -> bool:
        superusers = self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=guild.id
        )
        return user_id in superusers or user_id == guild.owner_id
