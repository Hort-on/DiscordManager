from modules.Management.Channel_factory.channel_scenarios import (
    SaveChannelToDBScenario,
    PermissionsScenario,
    WizardScenario,
    CompositeScenario,
    DeleteMessagesScenario,
    SaveChannelToDBForMessageScenario
)

class ChannelScenarioFactory:

    @staticmethod
    def for_permissions() -> PermissionsScenario:
        return PermissionsScenario()

    @staticmethod
    def for_db_save(config_key: str) -> SaveChannelToDBScenario:
        return SaveChannelToDBScenario(config_key)

    @staticmethod
    def for_db_message_save() -> SaveChannelToDBForMessageScenario:
        return SaveChannelToDBForMessageScenario()

    @staticmethod
    def for_wizard(parent, config_key: str) -> WizardScenario:
        return WizardScenario(parent, config_key)

    @staticmethod
    def for_message_deletion() -> DeleteMessagesScenario:
        return DeleteMessagesScenario()

    @staticmethod
    def for_full_setup(parent, config_key: str):
        return CompositeScenario(
            WizardScenario(parent, config_key),
            SaveChannelToDBScenario(config_key),
            PermissionsScenario()
        )
