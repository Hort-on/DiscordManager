from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.navigator import Navigator

import discord

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

from general_services.factories.channel_factory.channel_scenarios import ChannelScenario


class ChannelSelectorManager:
    def __init__(
            self,
            settings: SettingsStorage,
            navigator: Navigator,
            scenario: ChannelScenario,
            text_only=False,
            channels_with_users_only=False,
    ):

        self.navigator = navigator
        self.settings = settings
        self.scenario = scenario
        self.text = text_only
        self.channels_with_users_only = channels_with_users_only

    async def build_options(self, interaction: discord.Interaction) -> list[discord.SelectOption] | None:
        hidden_channels = self.settings.set_storage.for_set_get(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=interaction.guild_id
        )

        if self.text:
            channels = interaction.guild.text_channels
        else:
            channels = interaction.guild.voice_channels

            if self.channels_with_users_only:
                channels = [
                    vc for vc in channels
                    if len(vc.members) > 2
                ]

        return [
            discord.SelectOption(
                label=channel.name,
                value=str(channel.id)
            )
            for channel in channels if channel.id not in hidden_channels
        ]

    async def proceed_channel(self, interaction: discord.Interaction, value: list[str]) -> None:
        channel_id = int(value[0])
        channel = interaction.client.get_channel(channel_id)

        await self.scenario.on_selected_channel(interaction, channel=channel)
