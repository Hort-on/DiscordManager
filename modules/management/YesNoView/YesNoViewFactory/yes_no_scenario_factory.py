from database.db_factory.db_scenario_factory import DBScenarioFactory
from modules.management.YesNoView.YesNoViewFactory.yes_no_scenarios import StartConfigScenario, ConfirmationScenario


class YesNoViewFactory:
    @staticmethod
    def for_start_config(parent, config_key: str=None, on_decline_callback=None):
        return StartConfigScenario(parent, config_key, on_decline_callback)

    @staticmethod
    def for_confirmation(db: DBScenarioFactory,config_key: str):
        return ConfirmationScenario(db, config_key)