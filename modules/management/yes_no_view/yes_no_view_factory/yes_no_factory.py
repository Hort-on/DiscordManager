from modules.management.yes_no_view.yes_no_view_factory.yes_no_scenarios import ConfirmationScenario
from services.factories.db_factory.db_scenario_factory import DBScenarioFactory


class YesNoViewFactory:

    @staticmethod
    def for_confirmation(db_factory: DBScenarioFactory, config_key: str):
        return ConfirmationScenario(db_factory, config_key)
