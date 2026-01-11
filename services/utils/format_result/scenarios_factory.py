from core.main import BotController
from database.settings_storage.settings import SettingsStorage

from services.utils.format_result.scenarios import EditSettingsResultScenario


class ResultFactory:

    @staticmethod
    def for_settings_edit(settings: SettingsStorage):
        return EditSettingsResultScenario(settings)
