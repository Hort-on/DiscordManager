from database.db_factory.db_scenario_factory import DBScenarioFactory
from modules.configuration.starting_configuration import ConfigurationView
from modules.management.YesNoView.YesNoViewFactory.yes_no_scenarios import StartConfigScenario, ConfirmationScenario


class YesNoViewFactory:
    @staticmethod
    def for_start_config(
            parent: ConfigurationView,
            config_key: str = None,
            on_decline_callback=None
    ):
        return StartConfigScenario(parent, config_key, on_decline_callback)

    @staticmethod
    def for_confirmation(db_factory: DBScenarioFactory, config_key: str):
        return ConfirmationScenario(db_factory, config_key)
