import discord

from services.buttons.protection.admin_buttons_protection import FirewallButton


# TODO: оепепнахрх же ме рю ймнойю
class SameGameButton(FirewallButton):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='Show members with the same game roles',
            style=discord.ButtonStyle.blurple
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()
