import discord

from database.settings_storage.settings import SettingsStorage
from services.buttons.protection.admin_buttons_protection import FirewallButton
from services.factories.channel_factory.scenarios_factory import ChannelScenarioFactory
from services.modals.delete_msg_modal.del_msg_from_user import DeleteUserMessagesModal
from services.other_services.get_channel import ChannelSelectorManager


class DeleteUserMessageButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Delete message from users',
            style=discord.ButtonStyle.blurple
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        scenario = ChannelScenarioFactory.for_message_deletion(modal=DeleteUserMessagesModal)

        manager = ChannelSelectorManager(
            scenario=scenario,
            text_only=True
        )

        await manager.select_channel_type(interaction=interaction)
