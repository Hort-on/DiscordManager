import discord

from services.buttons.protection.admin_buttons_protection import FirewallButton
from services.factories.channel_factory.scenarios_factory import ChannelScenarioFactory
from services.modals.delete_msg_modal.del_msg import DeleteMessagesModal
from services.other_services.get_channel import ChannelSelectorManager
from services.utils.messages import GENERAL_MSGS as GM


class DeleteAnyMessageButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Delete message',
            style=discord.ButtonStyle.blurple
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        scenario = ChannelScenarioFactory.for_message_deletion(modal=DeleteMessagesModal)

        manager = ChannelSelectorManager(
            scenario=scenario,
            text_only=True
        )
        await manager.select_channel_type(interaction=interaction)

