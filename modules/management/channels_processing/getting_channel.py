import discord
from discord import ui

from services.factories.channel_factory import ChannelScenario
from services.utils.messages import GENERAL_MSGS


class ChannelTypeView(ui.View):
    def __init__(
            self,
            scenario: ChannelScenario,
            text_only=False,
            channels_with_users_only=False
    ):
        super().__init__(timeout=60)

        self.scenario = scenario
        self.channels_with_users_only = channels_with_users_only

        self.options = []

        if not channels_with_users_only:
            self.options.append(
                discord.SelectOption(
                    label="Text channel",
                    value="text"
                )
            )

        if not text_only:
            self.options.append(
                discord.SelectOption(
                    label="Voice channel",
                    value="voice"
                )
            )

        select = ui.Select(
            placeholder=GENERAL_MSGS.get("ask_channel_type_msg"),
            options=self.options
        )

        select.callback = self.select_channel_type
        self.add_item(select)

    async def select_channel_type(self, interaction: discord.Interaction):
        channel_type = self.children[0].values[0]

        if channel_type == "text":
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
                content="No channels found",
                view=None
            )
            return

        view = ChannelSelectView(channels, self.scenario)
        await interaction.edit_original_response(
            content="Please select a channel:",
            view=view
        )


class ChannelSelectView(ui.View):
    def __init__(self, channels, scenario: ChannelScenario):
        super().__init__(timeout=60)
        self.scenario = scenario

        options = [
            discord.SelectOption(
                label=channel.name,
                value=str(channel.id)
            )
            for channel in channels
        ]

        select = ui.Select(
            placeholder="Select channel",
            options=options
        )

        select.callback = self.on_select
        self.add_item(select)

    async def on_select(self, interaction: discord.Interaction):
        channel_id = int(self.children[0].values[0])
        channel = interaction.client.get_channel(channel_id)

        if not channel:
            await interaction.edit_original_response(
                content="Channel not found",
                view=None
            )
            return

        await self.scenario.on_channel_selected(interaction, channel=channel)

        await interaction.edit_original_response(
            content=f"```Selected channel: {channel.name}```",
            view=None
        )
