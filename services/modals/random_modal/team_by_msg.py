import discord

from services.buttons.randomizer_service.msg_team import RandomTeamByMsgService


class RandomTeamByMsgModal(discord.ui.Modal, title='Random teams manual'):
    def __init__(self):
        super().__init__()
        self.random_proceed = RandomTeamByMsgService()

    users_list = discord.ui.TextInput(
        label='List of users',
        placeholder='Please enter user names separated by coma',
        required=True,
        max_length=3
    )

    teams_quantity = discord.ui.TextInput(
        label='Teams quantity',
        placeholder='Please enter a number of commands',
        required=True,
        max_length=3
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.random_proceed.team_by_text_proceed(
            interaction,
            str(self.users_list.value),
            int(self.teams_quantity.value)
        )
