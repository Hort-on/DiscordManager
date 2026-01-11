import discord

from services.factories.channel_factory.channel_scenario_factory import ChannelScenarioFactory
from services.modals.delete_msg_modal.DeleteMessageUserModal import DeleteUserMessagesModal

from modules.management.channels_processing.getting_channel import ChannelTypeView

from services.utils.messages import GENERAL_MSGS as GM


class DeleteUserMessageButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Delete message from users',
            style=discord.ButtonStyle.blurple
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()

        scenario = ChannelScenarioFactory.for_message_deletion(DeleteUserMessagesModal)

        view = ChannelTypeView(scenario, text_only=True)
        await interaction.edit_original_response(
            content=GM.get('ask_channel_msg'),
            view=view
        )
