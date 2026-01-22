from services.factories.db_factory.db_scenario_factory import DBFactory
from services.yes_no_view.yes_no_view_factory.yes_no_scenarios import ConfirmationScenario, ForBirthdayScenario


class YesNoViewFactory:

    @staticmethod
    def for_confirmation(db_factory: DBFactory, config_key: str) -> ConfirmationScenario:
        return ConfirmationScenario(db_factory=db_factory, config_key=config_key)

    @staticmethod
    def for_birthday() -> ForBirthdayScenario:
        return ForBirthdayScenario()
