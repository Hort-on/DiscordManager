import discord

from Modules.Management.buttons.edit_settings_view.EnableDisableButton.EnableDisableView import EnableDisableView
from Modules.Management.getting_channel import ChannelTypeView
from db.messages import GENERAL_MESSAGES as GM


class ChoiceHandler:
    @staticmethod
    async def choice_procedure(interaction: discord.Interaction, value: str, feature_name: str) -> None:
        match value:
            case 'boolean':
                view = EnableDisableView(value)
                await interaction.followup.send(
                    content=f'Would you like to enable or disable {feature_name.replace("_", " ").title()}?',
                    view=view
                )
            case 'channel':
                view = ChannelTypeView(text_only=True, write_data_to_db=True, send_the_result=True)
                await interaction.followup.send(
                    content=GM.get('ask_channel_msg'),
                    view=view
                )
            case _:
                await interaction.followup.send('Unexpected error')
                return
