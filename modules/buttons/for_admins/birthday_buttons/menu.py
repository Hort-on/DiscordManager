import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.buttons.for_admins.birthday_buttons.menu_view import BirthdayMenuView


class BirthdayMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='🎂 Birthdays',
            style=discord.ButtonStyle.secondary
        )

    async def on_click(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.edit_original_response(
            content='🎂 Birthday management',
            view=BirthdayMenuView()
        )
