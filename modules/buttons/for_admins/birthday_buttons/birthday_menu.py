import discord

from modules.birthdays.birthday_repo import BirthdayManager
from modules.buttons.views.for_admins.birthday_menu import BirthdayMenuView

from services.buttons.protection.admin_buttons_protection import FirewallButton


class BirthdayMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self, birthday_manager: BirthdayManager):
        super().__init__(
            label='🎂 Birthdays',
            style=discord.ButtonStyle.secondary
        )
        self.birthday_manager = birthday_manager

    async def on_click(self, interaction: discord.Interaction):
        await interaction.edit_original_response(
            content='🎂 Birthday management',
            view=BirthdayMenuView(
                guild_id=interaction.guild_id,
                user_id=interaction.user.id,
                birthday_manager=self.birthday_manager
            )
        )
