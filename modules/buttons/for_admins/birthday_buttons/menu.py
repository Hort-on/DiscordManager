import discord

from modules.buttons.for_admins.birthday_buttons.menu_view import BirthdayMenuView
from modules.buttons.services.protection.admin_buttons_protection import FirewallButton


class BirthdayMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='🎂 Birthdays',
            style=discord.ButtonStyle.secondary
        )

    async def on_click(self, interaction: discord.Interaction):
        await interaction.edit_original_response(
            content='🎂 Birthday management',
            view=BirthdayMenuView().prepare(
                guild_id=interaction.guild_id,
                user_id=interaction.user.id
            )
        )
