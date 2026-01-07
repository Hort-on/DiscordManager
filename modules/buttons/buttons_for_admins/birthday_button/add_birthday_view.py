import discord

from services.modals.birthday_modal.BirthdayAddModal import AddBirthdayModal

from modules.birthdays.birthday_repo import BirthdayRepo


class AddBirthdayButton(discord.ui.Button):
    def __init__(self, birthday: BirthdayRepo):
        super().__init__(
            label="Add birthday",
            style=discord.ButtonStyle.blurple
        )
        self.birthday = birthday

    async def callback(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()
        await interaction.response.send_modal(AddBirthdayModal(self.birthday))
