from database.settings_storage.settings import SettingsStorage
from modules.birthdays.birthday_repo import BirthdayManager
from modules.management.yes_no_view.yes_no_view_factory.yes_no_scenarios import ConfirmationScenario

from services.factories.db_factory.db_scenario_factory import DBFactory


class YesNoViewFactory:

    @staticmethod
    def for_confirmation(
            settings: SettingsStorage,
            db_factory: DBFactory,
            birthday_manager: BirthdayManager,
            config_key: str
    ):
        return ConfirmationScenario(
            settings=settings,
            db_factory=db_factory,
            birthday_manager=birthday_manager,
            config_key=config_key
        )
