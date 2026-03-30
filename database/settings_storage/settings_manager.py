from enum import Enum, auto


class StorageTarget(Enum):
    SETTINGS = auto()
    SYSTEM_CHANNELS = auto()
    HIDDEN_CHANNELS = auto()
    CHANNELS_TO_SEND = auto()
    SUPERUSERS = auto()
    HIDDEN_ROLES = auto()
    LANGUAGE = auto()


class SetStorageManager:
    def __init__(
            self,
            mapping: dict[StorageTarget, dict[int, set[int]]]
    ):
        self._map = mapping

    def for_set_get(self, target: StorageTarget, guild_id: int) -> set[int]:
        return self._map[target].setdefault(guild_id, set())


class DictStorageManager:
    def __init__(self, mapping: dict[StorageTarget, dict[int, dict]]):
        self._map = mapping

    def get_all(self, target: StorageTarget, guild_id: int) -> dict:
        return self._map.get(target, {}).get(guild_id, {})

    def get_value(self, key: str | int, target: StorageTarget, guild_id: int):
        guild_data = self.get_all(target, guild_id)
        return guild_data.get(key)
