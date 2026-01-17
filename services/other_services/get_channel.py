import discord
from dependency_injector.wiring import inject, Provide

from core.bot_container import BotContainer
from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget
from services.drop_down_menu.drop_down_selector import DropMenuView
from services.factories.channel_factory.channel_scenarios import ChannelScenario
from services.utils.messages import GENERAL_MSGS


class ChannelSelectorManager:
    @inject
    def __init__(
            self,
            scenario: ChannelScenario,
            settings: SettingsStorage = Provide[BotContainer.settings],
            text_only=False,
            channels_with_users_only=False,
    ):
        super().__init__(timeout=60)

        self.settings = settings
        self.scenario = scenario
        self.text = text_only
        self.channels_with_users_only = channels_with_users_only

    async def select_channel_type(self, interaction: discord.Interaction):
        type_options = []

        if not self.channels_with_users_only:
            type_options.append(
                discord.SelectOption(
                    label='Text channel',
                    value='text'
                )
            )

        if not self.text:
            type_options.append(
                discord.SelectOption(
                    label='Voice channel',
                    value='voice'
                )
            )

        view = DropMenuView(
            options=type_options,
            placeholder=GENERAL_MSGS.get('ask_channel_type_msg'),
            callback=self._select_channel
        )

        await interaction.edit_original_response(
            content='',
            view=view
        )

    async def _select_channel(
            self,
            interaction: discord.Interaction,
            value: list[str]
    ):
        hidden_channels = self.settings.set_storage.for_set_get(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=interaction.guild_id
        )

        if value == 'text':
            channels = interaction.guild.text_channels
        else:
            channels = interaction.guild.voice_channels

            if self.channels_with_users_only:
                channels = [
                    vc for vc in channels
                    if len(vc.members) > 2
                ]

        if not channels:
            await interaction.edit_original_response(
                content='No channels found',
                view=None
            )
            return

        channel_options = [
            discord.SelectOption(
                label=channel.name,
                value=str(channel.id)
            )
            for channel in channels if channel.id not in hidden_channels
        ]

        view = DropMenuView(
            options=channel_options,
            placeholder='',
            callback=self._save_channel
        )

        await interaction.edit_original_response(
            content='',
            view=view
        )

    async def _save_channel(
            self,
            interaction: discord.Interaction,
            value: list[str]
    ):

        channel_id = int(value[0])
        channel = interaction.client.get_channel(channel_id)

        if not channel:
            await interaction.edit_original_response(
                content='Channel not found',
                view=None
            )
            return

        await self.scenario.on_channel_selected(interaction, channel=channel)

        await interaction.edit_original_response(
            content=f'```Selected channel: {channel.name}```',
            view=None
        )
