from database.db_factory.db_scenario_factory import DBScenarioFactory
from modules.management.Channel_factory.channel_scenarios import (
    SaveChannelToDBScenario,
    WizardScenario,
    CompositeScenario,
    DeleteMessagesScenario,
    SaveChannelToDBForMessageScenario
)

class ChannelScenarioFactory:

    @staticmethod
    def for_db_save(
            db_factory: DBScenarioFactory,
            config_key: str
    ) -> SaveChannelToDBScenario:

        return SaveChannelToDBScenario(
            db_factory,
            config_key
        )

    @staticmethod
    def for_db_message_save(
            db_factory: DBScenarioFactory
    ) -> SaveChannelToDBForMessageScenario:

        return SaveChannelToDBForMessageScenario(db_factory)

    @staticmethod
    def for_wizard(
            parent,
            db_factory: DBScenarioFactory,
            config_key: str
    ) -> WizardScenario:

        return WizardScenario(
            parent,
            db_factory,
            config_key
        )

    @staticmethod
    def for_message_deletion() -> DeleteMessagesScenario:
        return DeleteMessagesScenario()

    @staticmethod
    def for_full_setup(
            parent,
            db_factory: DBScenarioFactory,
            config_key: str
    ):
        return CompositeScenario(
            WizardScenario(
                parent,
                db_factory,
                config_key
            ),
            SaveChannelToDBScenario(
                db_factory,
                config_key
            ),
        )
