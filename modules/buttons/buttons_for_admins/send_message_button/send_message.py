import discord

from services.factories import DBScenarioFactory

from services.factories.channel_factory import ChannelScenarioFactory
from modules.management.channels_processing.getting_channel import ChannelTypeView

from services.utils.messages import SYSTEM_MSGS as SM


class SendMessageButton(discord.ui.Button):
    def __init__(self, db_factory: DBScenarioFactory):
        super().__init__(
            label='Send message',
            style=discord.ButtonStyle.blurple
        )
        self.db_factory = db_factory

    async def callback(self, interaction: discord.Interaction):
        self.view.disable_all_items()
        scenario = ChannelScenarioFactory.for_db_message_save(self.db_factory)

        view = ChannelTypeView(
            scenario,
            text_only=True
        )

        try:
            await interaction.user.send(SM.get('ask_private_channel_msg'), view=view)

            await interaction.edit_original_response(
                content=SM.get('ask_private_msg')
            )
        except discord.Forbidden:
            await interaction.edit_original_response(
                content=SM.get('send_message_failure_msg')
            )
