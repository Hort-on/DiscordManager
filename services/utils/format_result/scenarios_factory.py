from database.settings_storage.settings import SettingsStorage

from services.utils.format_result.scenarios import EditSettingsResultScenario


class ResultFactory:

    @staticmethod
    def for_settings_edit():
        return EditSettingsResultScenario()
