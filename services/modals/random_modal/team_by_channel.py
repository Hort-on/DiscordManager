import discord

from services.buttons.for_users.randomizer_service.channel_team import RandomTeamByChannelService


class RandomTeamByChannelModal(discord.ui.Modal, title='Random teams automatically'):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel
        self.random_proceed = RandomTeamByChannelService()

    teams_quantity = discord.ui.TextInput(
        label='Teams quantity',
        placeholder='Please enter a number of teams',
        required=True,
        max_length=2
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.random_proceed.team_by_channel_proceed(
            interaction,
            self.channel,
            int(self.teams_quantity.value)
        )
