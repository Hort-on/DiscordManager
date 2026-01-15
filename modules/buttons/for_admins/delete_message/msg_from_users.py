import discord

from services.buttons.protection.admin_buttons_protection import FirewallButton
from services.factories.channel_factory.scenarios_factory import ChannelScenarioFactory
from services.modals.delete_msg_modal.del_msg_from_user import DeleteUserMessagesModal
from services.other_services.get_channel import ChannelTypeView
from services.utils.messages import GENERAL_MSGS as GM


class DeleteUserMessageButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Delete message from users',
            style=discord.ButtonStyle.blurple
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        scenario = ChannelScenarioFactory.for_message_deletion(DeleteUserMessagesModal)

        view = ChannelTypeView(scenario, text_only=True)
        await interaction.edit_original_response(
            content=GM.get('ask_channel_msg'),
            view=view
        )
