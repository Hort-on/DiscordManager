import discord

from database.settings_storage.settings import SettingsStorage
from modules.birthdays.birthday_repo import BirthdayManager
from services.factories.channel_factory.scenarios_factory import ChannelScenarioFactory
from services.factories.db_factory.db_scenario_factory import DBFactory
from services.other_services.get_channel import ChannelSelectorManager
from services.utils.messages import EDIT_CONFIG_MSGS, SYSTEM_MSGS

from modules.management.yes_no_view.yes_no_view_factory.yes_no_factory import YesNoViewFactory
from modules.management.yes_no_view.view.yes_no import YesNoView


class ChoiceHandler:
    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBFactory,
            birthday_manager: BirthdayManager
    ):
        self.settings = settings
        self.db_factory = db_factory
        self.birthday_manager = birthday_manager

    async def choice_procedure(
            self,
            interaction: discord.Interaction,
            option_type: str,
            config_key: str
    ) -> None:

        match option_type:
            case 'boolean':
                scenario = YesNoViewFactory.for_confirmation(
                    settings=self.settings,
                    db_factory=self.db_factory,
                    birthday_manager=self.birthday_manager,
                    config_key=config_key
                )

                view = YesNoView(scenario=scenario)

                await interaction.edit_original_response(
                    content=EDIT_CONFIG_MSGS.get('editing_feature_msg').format(
                        feature={config_key.replace('_', ' ').title()}),
                    view=view
                )

            case 'channel':
                scenario = ChannelScenarioFactory.for_db_save(
                    db_factory=self.db_factory,
                    config_key=config_key
                )

                manager = ChannelSelectorManager(
                    scenario=scenario,
                    settings=self.settings,
                    text_only=True
                )

                await manager.select_channel_type(interaction=interaction)

            case _:
                await interaction.edit_original_response(
                    content=SYSTEM_MSGS.get('failure_msg')
                )
                return
