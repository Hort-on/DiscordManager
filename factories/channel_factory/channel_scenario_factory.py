
from factories.channel_factory.channel_scenarios import (
    SaveChannelToDBScenario,
    DeleteMessagesScenario,
    SaveChannelToDBForMessageScenario
)
from factories.db_factory.db_scenario_factory import DBScenarioFactory


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
    def for_message_deletion(modal) -> DeleteMessagesScenario:
        return DeleteMessagesScenario(modal)
