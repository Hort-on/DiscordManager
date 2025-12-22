import discord

from modules.Management.Channel_factory.channel_scenario_factory import ChannelScenarioFactory
from modules.Management.channels_processing.getting_channel import ChannelTypeView


class SetPermissionButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Set permissions',
            style=discord.ButtonStyle.blurple
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.disable_all_items()
        scenario = ChannelScenarioFactory.for_permissions()
        view = ChannelTypeView(scenario)

        await interaction.response.send_message(
            'Please select the type of channel:',
            view=view,
            ephemeral=True,
            delete_after=600
        )
