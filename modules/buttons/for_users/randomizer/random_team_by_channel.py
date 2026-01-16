import discord

from services.buttons.protection.admin_buttons_protection import FirewallButton
from services.other_services.get_channel import ChannelSelectorManager
from services.factories.channel_factory.scenarios_factory import ChannelScenarioFactory


class RandomTeamByChannel(FirewallButton):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='Random team by channel',
            style=discord.ButtonStyle.secondary
        )

    async def on_click(self, interaction: discord.Interaction):
        scenario = ChannelScenarioFactory.for_random_selection()

        manager = ChannelSelectorManager(
            scenario=scenario,
            channels_with_users_only=True
        )

        await manager.select_channel_type(interaction)
