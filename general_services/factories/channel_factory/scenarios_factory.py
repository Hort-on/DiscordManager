from general_services.factories.channel_factory.channel_scenarios import (
    SaveChannelToDBScenario,
    SaveChannelToDBForMessageScenario,
    RandomSelection
)


class ChannelFactory:

    @staticmethod
    def for_db_save(config_key: str) -> SaveChannelToDBScenario:
        return SaveChannelToDBScenario(config_key)

    @staticmethod
    def for_db_message_save() -> SaveChannelToDBForMessageScenario:
        return SaveChannelToDBForMessageScenario()

    @staticmethod
    def for_random_selection() -> RandomSelection:
        return RandomSelection()
