import discord

from modules.birthdays.birthday_repo import BirthdayManager

from services.modals.birthday_modal.addition import AddBirthdayModal


class AddBirthdayButton(discord.ui.Button):
    def __init__(self, birthday_manager: BirthdayManager):
        super().__init__(
            label="Add birthday",
            style=discord.ButtonStyle.blurple
        )
        self.birthday_manager = birthday_manager

    async def callback(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()
        await interaction.response.send_modal(AddBirthdayModal(self.birthday_manager))
