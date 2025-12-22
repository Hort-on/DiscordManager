import discord

from YesNoView.YesNoViewFactory.yes_no_factory import YesNoViewFactory
from YesNoView.view.YesNoView import YesNoView
from modules.Management.Channel_factory.channel_scenario_factory import ChannelScenarioFactory
from modules.Management.channels_processing.getting_channel import ChannelTypeView
from utils.messages import GENERAL_MESSAGES as GM


class ChoiceHandler:
    @staticmethod
    async def choice_procedure(interaction: discord.Interaction, option_type: str, config_key: str) -> None:
        match option_type:
            case 'boolean':
                scenario = YesNoViewFactory.for_confirmation(config_key)
                view = YesNoView(scenario)
                await interaction.edit_original_response(
                    content=f'Would you like to enable or disable {config_key.replace("_", " ").title()}?',
                    view=view
                )

            case 'channel':
                scenario = ChannelScenarioFactory.for_db_save(config_key)
                view = ChannelTypeView(scenario, text_only=True)
                await interaction.edit_original_response(
                    content=GM.get('ask_channel_msg'),
                    view=view
                )

            case _:
                await interaction.edit_original_response(content='Unexpected error')
                return
