from enum import Enum, auto


class StorageTarget(Enum):
    SETTINGS = auto()
    SELECTED_CHANNELS = auto()
    HIDDEN_CHANNELS = auto()
    CHANNELS_TO_SEND = auto()
    SUPERUSERS = auto()
    HIDDEN_ROLES = auto()


class SetStorageManager:
    def __init__(
            self,
            mapping: dict[StorageTarget, dict[int, set[int]]]
    ):
        self._map = mapping

    def add_for_set(self, target: StorageTarget, guild_id: int, value: set[int]) -> None:
        self._map[target].setdefault(guild_id, set()).update(value)

    def get_for_set(self, target: StorageTarget, guild_id: int) -> set[int]:
        return self._map.get(target, {}).get(guild_id, set())

    def remove_for_set(self, target: StorageTarget, guild_id: int, value) -> None:
        self._map[target].get(guild_id, set()).difference_update(value)


class DictStorageManager:
    def __init__(self, mapping: dict[StorageTarget, dict[int, dict]]):
        self._map = mapping

    def set_for_dict(self, target: StorageTarget, guild_id: int, key, value) -> None:
        self._map[target].setdefault(guild_id, {})[key] = value

    def get_for_dict(self, target: StorageTarget, guild_id: int, key):
        return self._map.get(target, {}).get(guild_id, {}).get(key)

    def get_for_dict_all(self, target: StorageTarget, guild_id: int) -> dict:
        return self._map.get(target, {}).get(guild_id, {})

    def remove_for_dict(self, target: StorageTarget, guild_id: int, key) -> None:
        self._map[target].get(guild_id, {}).pop(key, None)
