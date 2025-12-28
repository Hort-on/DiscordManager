import discord

from database.db_factory.db_scenario_factory import DBScenarioFactory
from modules.management.Channel_factory.channel_scenario_factory import ChannelScenarioFactory
from modules.management.YesNoView.YesNoViewFactory.yes_no_scenario_factory import YesNoViewFactory
from modules.management.YesNoView.view.YesNoView import YesNoView
from modules.management.channels_processing.getting_channel import ChannelTypeView
from utils.messages import GENERAL_MSGS, EDIT_CONFIG_MSGS, SYSTEM_MSGS


class ChoiceHandler:
    def __init__(self, db: DBScenarioFactory):
        self.db = db

    async def choice_procedure(self, interaction: discord.Interaction, option_type: str, config_key: str) -> None:
        match option_type:
            case 'boolean':
                scenario = YesNoViewFactory.for_confirmation(
                    self.db,
                    config_key
                )

                view = YesNoView(scenario)

                await interaction.edit_original_response(
                    content=EDIT_CONFIG_MSGS.get('editing_feature_msg').format(
                        feature={config_key.replace("_", " ").title()}),
                    view=view
                )

            case 'channel':
                scenario = ChannelScenarioFactory.for_db_save(
                    self.db,
                    config_key
                )

                view = ChannelTypeView(
                    scenario,
                    text_only=True
                )

                await interaction.edit_original_response(
                    content=GENERAL_MSGS.get('ask_channel_msg'),
                    view=view
                )

            case _:
                await interaction.edit_original_response(
                    content=SYSTEM_MSGS.get('failure_msg')
                )
                return
