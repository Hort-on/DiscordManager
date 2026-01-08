import discord


class RandomTeamManualModal(discord.ui.Modal, title='Random teams manual'):
    def __init__(self):
        super().__init__()

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
        ...
