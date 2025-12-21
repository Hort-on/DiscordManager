import discord

from modules.buttons.buttons_for_admins.edit_settings_button.views.EnableDisableView import EnableDisableView
from modules.Management.Channel_factory.channel_scenario_factory import ChannelScenarioFactory
from modules.Management.getting_channel import ChannelTypeView
from utils.messages import GENERAL_MESSAGES as GM


class ChoiceHandler:
    @staticmethod
    async def choice_procedure(interaction: discord.Interaction, value: str, feature_name: str) -> None:
        match value:
            case 'boolean':
                view = EnableDisableView(value)
                await interaction.edit_original_response(
                    content=f'Would you like to enable or disable {feature_name.replace("_", " ").title()}?',
                    view=view
                )

            case 'channel':
                scenario = ChannelScenarioFactory.for_db_save()
                view = ChannelTypeView(scenario, text_only=True)
                await interaction.edit_original_response(
                    content=GM.get('ask_channel_msg'),
                    view=view
                )

            case _:
                await interaction.edit_original_response(content='Unexpected error')
                return
