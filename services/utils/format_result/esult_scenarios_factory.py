from database.settings_storage.settings_storage import SettingsStorage

from services.factories.db_factory.db_scenario_factory import DBScenarioFactory

from services.utils.format_result.result_scenarios import EditSettingsResultScenario


class ResultFactory:

    @staticmethod
    def for_settings_edit(db_factory: DBScenarioFactory, settings: SettingsStorage):
        return EditSettingsResultScenario(db_factory, settings)
