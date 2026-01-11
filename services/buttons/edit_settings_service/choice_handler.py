import discord

from services.factories.channel_factory.scenarios_factory import ChannelScenarioFactory
from services.factories.db_factory.db_scenario_factory import DBScenarioFactory

from services.utils.messages import GENERAL_MSGS, EDIT_CONFIG_MSGS, SYSTEM_MSGS

from modules.management.yes_no_view.yes_no_view_factory.yes_no_factory import YesNoViewFactory
from modules.management.yes_no_view.view.yes_no import YesNoView
from services.other_services.get_channel import ChannelTypeView


class ChoiceHandler:
    def __init__(self, db_factory: DBScenarioFactory):
        self.db_factory = db_factory

    async def choice_procedure(
            self,
            interaction: discord.Interaction,
            option_type: str,
            config_key: str
    ) -> None:

        match option_type:
            case 'boolean':
                scenario = YesNoViewFactory.for_confirmation(
                    self.db_factory,
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
                    self.db_factory,
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
