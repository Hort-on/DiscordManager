import discord

from modules.birthdays.birthday_repo import BirthdayRepo


class AddBirthdayButton(discord.ui.Button):
    def __init__(self, birthday: BirthdayRepo):
        super().__init__(
            label="Show members with the same game roles",
            style=discord.ButtonStyle.blurple
        )
        self.birthday = birthday

    async def callback(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()
