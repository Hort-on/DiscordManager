import discord

from services.button_services.randomizer_service.RandomTeamAutoService import RandomTeamAutoService


class RandomTeamAutoModal(discord.ui.Modal, title='Random teams automatically'):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel
        self.random_proceed = RandomTeamAutoService()

    teams_quantity = discord.ui.TextInput(
        label='Teams quantity',
        placeholder='Please enter a number of teams',
        required=True,
        max_length=2
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.random_proceed.random_team_proceed(
            interaction,
            self.channel,
            int(self.teams_quantity.value)
        )
