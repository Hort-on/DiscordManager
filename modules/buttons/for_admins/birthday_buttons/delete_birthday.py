import discord

from modules.birthdays.birthday_repo import BirthdayManager

from services.buttons.protection.admin_buttons_protection import FirewallButton
from services.modals.birthday_modal.deletion import DeleteBirthdayModal


class DeleteBirthdayButton(FirewallButton):
    scope = 'admin'

    def __init__(self, birthday_manager: BirthdayManager):
        super().__init__(
            label='Delete birthday',
            style=discord.ButtonStyle.red
        )
        self.birthday_manager = birthday_manager

    async def on_click(self, interaction: discord.Interaction):
        self.view.disable_all_items()
        await interaction.response.send_modal(DeleteBirthdayModal(self.birthday_manager))
