from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.navigator import Navigator

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton

from modules.buttons.for_users.randomizer.modals import (
    RandomNumModal,
    RandomWordModal,
    RandomTeamByMsgModal
)

from general_services.factories.channel_factory.scenarios_factory import ChannelFactory
from general_services.other_services.get_channel import ChannelSelectorManager


class RandomNumButton(FirewallButton):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='Random number',
            style=discord.ButtonStyle.secondary
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(RandomNumModal())


class RandomWordButton(FirewallButton):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='Random word',
            style=discord.ButtonStyle.secondary
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(RandomWordModal())


class RandomTeamByMsg(FirewallButton):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='Random team by message',
            style=discord.ButtonStyle.secondary
        )

    async def on_click(self, interaction: discord.Interaction):
        await interaction.response.send_modal(RandomTeamByMsgModal())


class RandomTeamByChannel(FirewallButton):
    scope = 'user'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Random team by channel',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction):
        scenario = ChannelFactory.for_random_selection()

        manager = ChannelSelectorManager(
            navigator=self.navigator,
            scenario=scenario,
            channels_with_users_only=True
        )

        await manager.select_channel(interaction=interaction)
