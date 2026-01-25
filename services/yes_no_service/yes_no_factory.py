from __future__ import annotations

from services.factories.db_factory.db_scenario_factory import DBFactory
from services.yes_no_service.yes_no_scenarios import ConfirmationScenario, ForBirthdayScenario

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.buttons.navigator import Navigator


class YesNoViewFactory:

    def for_confirmation(
            self,
            db_factory: DBFactory,
            navigator: Navigator,
            config_key: str
    ) -> ConfirmationScenario:
        return ConfirmationScenario(
            db_factory=db_factory,
            navigator=navigator,
            yes_no_factory=self,
            config_key=config_key
        )

    @staticmethod
    def for_birthday() -> ForBirthdayScenario:
        return ForBirthdayScenario()
