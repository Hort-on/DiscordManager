from modules.management.yes_no_view.yes_no_view_factory.yes_no_scenarios import ConfirmationScenario


class YesNoViewFactory:

    @staticmethod
    def for_confirmation(config_key: str):
        return ConfirmationScenario(config_key=config_key)
