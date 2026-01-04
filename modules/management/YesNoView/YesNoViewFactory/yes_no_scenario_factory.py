from factories.db_factory import DBScenarioFactory

from modules.management.YesNoView.YesNoViewFactory.yes_no_scenarios import ConfirmationScenario


class YesNoViewFactory:

    @staticmethod
    def for_confirmation(db_factory: DBScenarioFactory, config_key: str):
        return ConfirmationScenario(db_factory, config_key)
