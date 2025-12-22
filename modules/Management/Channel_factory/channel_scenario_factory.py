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
    def for_permissions():
        return PermissionsScenario()

    @staticmethod
    def for_db_save(config_key):
        return SaveChannelToDBScenario(config_key)

    @staticmethod
    def for_db_message_save():
        return SaveChannelToDBForMessageScenario()

    @staticmethod
    def for_wizard(parent, config_key):
        return WizardScenario(parent, config_key)

    @staticmethod
    def for_message_deletion():
        return DeleteMessagesScenario()

    @staticmethod
    def for_full_setup(parent, config_key):
        return CompositeScenario(
            WizardScenario(parent, config_key),
            SaveChannelToDBScenario(),
            PermissionsScenario()
        )
