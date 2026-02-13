from ui.yes_no_service.yes_no_scenarios import ForBirthdayScenario


class YesNoViewFactory:

    @staticmethod
    def for_birthday() -> ForBirthdayScenario:
        return ForBirthdayScenario()
