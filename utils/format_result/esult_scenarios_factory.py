from factories.db_factory import DBScenarioFactory
from database.settings_storage.settings_storage import SettingsStorage

from utils.format_result.result_scenarios import FirstConfirmationScenario, EditSettingsResultScenario


class ResultFactory:

    @staticmethod
    def for_settings_edit(db_factory: DBScenarioFactory, settings: SettingsStorage):
        return EditSettingsResultScenario(db_factory, settings)
