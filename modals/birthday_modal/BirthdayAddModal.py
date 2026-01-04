import discord

from modules.birthdays.birthday_repo import BirthdayRepo

from .BirthdayService import AddBirthdayService


class AddBirthdayModal(discord.ui.Modal, title='Please enter a birthday:'):
    def __init__(self, birthday: BirthdayRepo):
        super().__init__()
        self.birthday = birthday
        self.b_day_service = AddBirthdayService(self.birthday)

    username = discord.ui.TextInput(
        label='Discord username',
        placeholder='user123',
        required=True
    )

    birthday_input = discord.ui.TextInput(
        label='Birthday (DD.MM)',
        placeholder='31.12',
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.b_day_service.process(
            interaction=interaction,
            username=self.username.value,
            birthday=self.birthday_input.value
        )
