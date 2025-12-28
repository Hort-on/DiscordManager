import discord

from modules.management.Channel_factory.channel_scenario_factory import ChannelScenarioFactory
from modules.management.channels_processing.getting_channel import ChannelTypeView
from utils.messages import GENERAL_MSGS as GM


class DeleteMessageButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Delete message',
            style=discord.ButtonStyle.blurple
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()
        scenario = ChannelScenarioFactory.for_message_deletion()
        view = ChannelTypeView(scenario, text_only=True)
        await interaction.response.send_message(
            content=GM.get('ask_channel_msg'),
            view=view
        )
