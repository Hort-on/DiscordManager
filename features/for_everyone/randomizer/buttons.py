from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.for_everyone.randomizer.modals import RandomNumModal, RandomWordModal, RandomTeamByMsgModal

from general_services.factories.channel_factory.scenarios_factory import ChannelFactory

if TYPE_CHECKING:
    from core.navigator import Navigator


class RandomNumButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Random number',
            style=discord.ButtonStyle.secondary
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(RandomNumModal())


class RandomWordButton(discord.ui.Button):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='Random word',
            style=discord.ButtonStyle.secondary
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(RandomWordModal())


class RandomTeamByMsg(discord.ui.Button):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='Random team by message',
            style=discord.ButtonStyle.secondary
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(RandomTeamByMsgModal())


class RandomTeamByChannel(discord.ui.Button):
    scope = 'user'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Random team by channel',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def callback(self, interaction: discord.Interaction):
        scenario = ChannelFactory.for_random_selection()

        manager = ChannelSelectorManager( # TODO: має бути flow
            navigator=self.navigator,
            scenario=scenario,
            channels_with_users_only=True
        )

        await manager.select_channel(interaction=interaction)
