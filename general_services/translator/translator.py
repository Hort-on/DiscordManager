from __future__ import annotations

from typing import TYPE_CHECKING

from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage


class Translator:
    def __init__(self, settings: SettingsStorage):
        self.settings = settings

    def t(self, guild_id: int, section: str, key: str, **kwargs):
        language = self.settings.dict_storage.get_all(
            target=StorageTarget.LANGUAGE,
            guild_id=guild_id
        )

        text = language.get(section, {}).get(key, key)
        return text.format(**kwargs)
