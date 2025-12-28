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
            db: DBScenarioFactory,
            config_key: str
    ) -> SaveChannelToDBScenario:

        return SaveChannelToDBScenario(
            db,
            config_key
        )

    @staticmethod
    def for_db_message_save(
            db: DBScenarioFactory
    ) -> SaveChannelToDBForMessageScenario:

        return SaveChannelToDBForMessageScenario(db)

    @staticmethod
    def for_wizard(
            parent,
            db: DBScenarioFactory,
            config_key: str
    ) -> WizardScenario:

        return WizardScenario(
            parent,
            db,
            config_key
        )

    @staticmethod
    def for_message_deletion() -> DeleteMessagesScenario:
        return DeleteMessagesScenario()

    @staticmethod
    def for_full_setup(
            parent,
            db: DBScenarioFactory,
            config_key: str
    ):
        return CompositeScenario(
            WizardScenario(
                parent,
                db,
                config_key
            ),
            SaveChannelToDBScenario(
                db,
                config_key
            ),
        )
