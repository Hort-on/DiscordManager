import discord

from database.db_factory.db_scenario_factory import DBScenarioFactory
from modules.management.Channel_factory.channel_scenario_factory import ChannelScenarioFactory
from modules.management.channels_processing.getting_channel import ChannelTypeView


class SendMessageButton(discord.ui.Button):
    def __init__(self, db: DBScenarioFactory):
        super().__init__(
            label='Send message',
            style=discord.ButtonStyle.blurple
        )
        self.db = db

#TODO: добавити ці повідомлення у загальний список messages
    async def callback(self, interaction: discord.Interaction):
        self.view.disable_all_items()
        try:
            scenario = ChannelScenarioFactory.for_db_message_save(self.db)
            view = ChannelTypeView(scenario, text_only=True)
            await interaction.user.send('```Please select the channel where the messages will be sent.:```',
                                        view=view)

            await interaction.edit_original_response(
                content='```Please check your private messages to select a channel.```')
        except discord.Forbidden:
            await interaction.edit_original_response(
                content='```Failed to send a message to your private messages. Please check your privacy settings.```'
            )
