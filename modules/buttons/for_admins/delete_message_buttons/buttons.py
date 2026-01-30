from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.buttons.for_admins.delete_message_buttons.modals import DeleteMessagesModal, DeleteUserMessagesModal

from services.factories.channel_factory.scenarios_factory import ChannelFactory
from services.other_services.get_channel import ChannelSelectorManager


class DeleteAnyMessageButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Delete message',
            style=discord.ButtonStyle.blurple
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        scenario = ChannelFactory.for_message_deletion(modal=DeleteMessagesModal)

        manager = ChannelSelectorManager(
            navigator=self.navigator,
            scenario=scenario,
            text_only=True
        )
        await manager.select_channel_type()


class DeleteUserMessageButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Delete message from users',
            style=discord.ButtonStyle.blurple
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        scenario = ChannelFactory.for_message_deletion(modal=DeleteUserMessagesModal)

        manager = ChannelSelectorManager(
            navigator=self.navigator,
            scenario=scenario,
            text_only=True
        )

        await manager.select_channel_type()
