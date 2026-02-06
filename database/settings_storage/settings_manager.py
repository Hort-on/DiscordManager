from enum import Enum, auto


class StorageTarget(Enum):
    SETTINGS = auto()
    SYSTEM_CHANNELS = auto()
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

    def for_set_add(self, target: StorageTarget, guild_id: int, value: set[int]) -> None:
        self._map[target].setdefault(guild_id, set()).update(value)

    def for_set_get(self, target: StorageTarget, guild_id: int) -> set[int]:
        return self._map.get(target, {}).get(guild_id, set())

    def for_set_get_all(self, target: StorageTarget, guild_id: int) -> set[int]:
        return self._map.get(target, {}).get(guild_id, set())

    def for_set_remove(self, target: StorageTarget, guild_id: int, value) -> None:
        self._map[target].get(guild_id, set()).difference_update(value)


class DictStorageManager:
    def __init__(self, mapping: dict[StorageTarget, dict[int, dict]]):
        self._map = mapping

    def for_dict_set(self, target: StorageTarget, guild_id: int, key, value) -> None:
        self._map[target].setdefault(guild_id, {})[key] = value

    def for_dict_get(self, *keys, target: StorageTarget, guild_id: int) -> dict[str, int]:
        data = self._map.get(target, {}).get(guild_id, {})
        return {key: data.get(key) for key in keys}

    def for_dict_get_all(self, target: StorageTarget, guild_id: int) -> dict:
        return self._map.get(target, {}).get(guild_id, {})

    def for_dict_remove(
            self,
            target: StorageTarget,
            guild_id: int,
            keys,
    ) -> None:
        guild_data = self._map[target].get(guild_id)
        if target == StorageTarget.SYSTEM_CHANNELS:
            for key in keys:
                if key in guild_data:
                    guild_data[key] = None
            return

        for key in keys:
            guild_data.pop(key, None)
