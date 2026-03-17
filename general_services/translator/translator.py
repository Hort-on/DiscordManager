from __future__ import annotations

from typing import TYPE_CHECKING

from database.settings_storage.settings_manager import StorageTarget

from general_services.translator.translations import TRANSLATIONS

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage


class Translator:
    def __init__(self, settings: SettingsStorage):
        self.settings = settings

    def t(self, guild_id: int, section: str, key: str, **kwargs):
        lang_code = self.settings.dict_storage.get_value(
            key='language',
            target=StorageTarget.SETTINGS,
            guild_id=guild_id
        ) or 'en'

        language = TRANSLATIONS.get(lang_code, TRANSLATIONS['en'])

        text = language.get(section, {}).get(key)

        if text is None:
            text = TRANSLATIONS['en'].get(section, {}).get(key, key)

        return text.format(**kwargs)
