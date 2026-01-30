from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.container import BotContainer
    from services.buttons.navigator import Navigator

import discord

from core.container import AppContainer

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

from services.drop_down_menu.drop_down_selector import DropMenuView
from services.factories.channel_factory.channel_scenarios import ChannelScenario
from services.utils.messages import GENERAL_MSGS


class ChannelSelectorManager:
    def __init__(
            self,
            navigator: Navigator,
            scenario: ChannelScenario,
            text_only=False,
            channels_with_users_only=False,
    ):
        container: BotContainer = AppContainer.get()

        self.navigator = navigator
        self.settings: SettingsStorage = container.settings
        self.scenario = scenario
        self.text = text_only
        self.channels_with_users_only = channels_with_users_only

    async def select_channel_type(self, interaction: discord.Interaction):
        print('ChannelSelectorManager - select_channel_type: OK')
        options = []

        if not self.channels_with_users_only:
            options.append(
                discord.SelectOption(
                    label='Text channel',
                    value='text'
                )
            )

        if not self.text:
            options.append(
                discord.SelectOption(
                    label='Voice channel',
                    value='voice'
                )
            )

        print('ChannelSelectorManager - select_channel_type - options: OK')
        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder=GENERAL_MSGS.get('ask_channel_type_msg'),
            callback=self._select_channel
        )

        print('ChannelSelectorManager - select_channel_type - view: OK')

        await interaction.response.edit_message(view=view)

    async def _select_channel(self, interaction: discord.Interaction, value: list[str]):
        hidden_channels = self.settings.set_storage.for_set_get(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=interaction.guild_id
        )

        if value[0] == 'text':
            channels = interaction.guild.text_channels
        else:
            channels = interaction.guild.voice_channels

            if self.channels_with_users_only:
                channels = [
                    vc for vc in channels
                    if len(vc.members) > 2
                ]

        if not channels:
            await interaction.response.edit_message(
                content='No channels found',
                view=None
            )
            return ''

        channel_options = [
            discord.SelectOption(
                label=channel.name,
                value=str(channel.id)
            )
            for channel in channels if channel.id not in hidden_channels
        ]

        return DropMenuView(
            navigator=self.navigator,
            options=channel_options,
            placeholder='',
            callback=self._save_channel
        )

    async def _save_channel(
            self,
            interaction: discord.Interaction,
            value: list[str]
    ):

        channel_id = int(value[0])
        channel = interaction.client.get_channel(channel_id)

        if not channel:
            return ''

        await self.scenario.on_channel_selected(interaction, channel=channel)

        return f'```Selected channel: {channel.name}```'
