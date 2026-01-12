import discord


class SuperusersMenuButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Superusers management',
            style = discord.ButtonStyle.green
        )
