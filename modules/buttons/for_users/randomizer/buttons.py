import discord

from modules.buttons.for_users.randomizer.modals import RandomNumModal, RandomWordModal, RandomTeamByMsgModal
from modules.buttons.services.protection.admin_buttons_protection import FirewallButton

from services.factories.channel_factory.scenarios_factory import ChannelFactory
from services.other_services.get_channel import ChannelSelectorManager


class RandomNumButton(FirewallButton):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='Random number',
            style=discord.ButtonStyle.secondary
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        await interaction.send_modal(RandomNumModal())


class RandomWordButton(FirewallButton):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='Random number',
            style=discord.ButtonStyle.secondary
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        await interaction.send_modal(RandomWordModal())


class RandomTeamByMsg(FirewallButton):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='Random number',
            style=discord.ButtonStyle.secondary
        )

    async def on_click(self, interaction: discord.Interaction):
        await interaction.send_modal(RandomTeamByMsgModal())


class RandomTeamByChannel(FirewallButton):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='Random team by channel',
            style=discord.ButtonStyle.secondary
        )

    async def on_click(self, interaction: discord.Interaction):
        scenario = ChannelFactory.for_random_selection()

        manager = ChannelSelectorManager(
            scenario=scenario,
            channels_with_users_only=True
        )

        await manager.select_channel_type(interaction)
