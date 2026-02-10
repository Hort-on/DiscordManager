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

    def for_set_get(self, target: StorageTarget, guild_id: int) -> set[int]:
        return self._map.get(target, {}).get(guild_id, set())

    def for_set_add(self, target: StorageTarget, guild_id: int, value: set[int]) -> None:
        guild_data = (
            self._map[target]
            .setdefault(guild_id, set())
        )

        guild_data.update(value)

    def for_set_remove(self, target: StorageTarget, guild_id: int, value) -> None:
        guild_data = (
            self._map[target]
            .get(guild_id, set())
        )

        guild_data.difference_update(value)


class DictStorageManager:
    def __init__(self, mapping: dict[StorageTarget, dict[int, dict]]):
        self._map = mapping

    def for_dict_update(self, target: StorageTarget, guild_id: int, data: dict) -> None:
        guild_data = (
            self._map
            .setdefault(target, {})
            .setdefault(guild_id, {})
        )

        for key, value in data.items():
            guild_data[key] = value

    def for_dict_get(self, *keys, target: StorageTarget, guild_id: int) -> dict:
        guild_data = (
            self._map
            .get(target, {})
            .get(guild_id, {})
        )

        if not keys:
            return guild_data

        return {key: guild_data.get(key) for key in keys}

    def for_dict_delete(self, target: StorageTarget, guild_id: int, data: set[int]):
        guild_data = (
            self._map
            .get(target, {})
            .get(guild_id, {})
        )

        for key in data:
            guild_data.pop(key, None)
