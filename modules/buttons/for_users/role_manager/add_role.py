import discord

from services.buttons.protection.admin_buttons_protection import FirewallButton


class AddRoleButton(FirewallButton):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='Add role',
            style=discord.ButtonStyle.blurple
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()
        await interaction.response dag