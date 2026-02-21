from enum import Enum, auto


class StorageTarget(Enum):
    SETTINGS = auto()
    SYSTEM_CHANNELS = auto()
    HIDDEN_CHANNELS = auto()
    CHANNELS_TO_SEND = auto()
    SUPERUSERS = auto()
    HIDDEN_ROLES = auto()
    BAD_WORDS = auto()


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

    def for_dict_get(self, *keys, target: StorageTarget, guild_id: int) -> dict:
        guild_data = self._map.get(target, {}).get(guild_id, {})

        if not keys:
            return guild_data

        return {key: guild_data.get(key) for key in keys}
