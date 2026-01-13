import discord

from services.buttons.protection.admin_buttons_protection import FirewallButton


class SuperusersMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Superusers management',
            style=discord.ButtonStyle.green
        )


