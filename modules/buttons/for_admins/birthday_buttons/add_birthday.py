import discord

from modules.birthdays.birthday_repo import BirthdayManager
from services.buttons.protection.admin_buttons_protection import FirewallButton

from services.modals.birthday_modal.addition import AddBirthdayModal


class AddBirthdayButton(FirewallButton):
    scope = 'admin'

    def __init__(self, birthday_manager: BirthdayManager):
        super().__init__(
            label="Add birthday",
            style=discord.ButtonStyle.blurple
        )
        self.birthday_manager = birthday_manager

    async def on_click(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(AddBirthdayModal(self.birthday_manager))
