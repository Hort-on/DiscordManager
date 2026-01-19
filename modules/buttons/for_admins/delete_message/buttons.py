import discord

from modules.buttons.for_admins.delete_message.modals import DeleteMessagesModal, DeleteUserMessagesModal
from modules.buttons.services.protection.admin_buttons_protection import FirewallButton

from services.factories.channel_factory.scenarios_factory import ChannelFactory
from services.other_services.get_channel import ChannelSelectorManager


class DeleteAnyMessageButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Delete message',
            style=discord.ButtonStyle.blurple
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        scenario = ChannelFactory.for_message_deletion(modal=DeleteMessagesModal)

        manager = ChannelSelectorManager(
            scenario=scenario,
            text_only=True
        )
        await manager.select_channel_type(interaction=interaction)


class DeleteUserMessageButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Delete message from users',
            style=discord.ButtonStyle.blurple
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        scenario = ChannelFactory.for_message_deletion(modal=DeleteUserMessagesModal)

        manager = ChannelSelectorManager(
            scenario=scenario,
            text_only=True
        )

        await manager.select_channel_type(interaction=interaction)
