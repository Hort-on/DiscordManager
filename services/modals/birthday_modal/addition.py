import discord

from modules.birthdays.birthday_repo import BirthdayManager

from services.button_services.birthday_service.add_birthday import AddBirthdayService


class AddBirthdayModal(discord.ui.Modal, title='Please enter a birthday:'):
    def __init__(self, birthday_manager: BirthdayManager):
        super().__init__()
        self.b_day_service = AddBirthdayService(birthday_manager)

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
        await self.b_day_service.add_process(
            interaction=interaction,
            username=self.username.value,
            birthday=self.birthday_input.value
        )
