import discord

from modules.birthdays.birthday_repo import BirthdayRepo

from services.button_services.birthday_service.DeleteBirthdayService import DeleteBirthdayService


class DeleteBirthdayModal(discord.ui.Modal, title='Delete birthday'):
    def __init__(self, birthday: BirthdayRepo):
        super().__init__()
        self.birthday = birthday
        self.b_day_service = DeleteBirthdayService(self.birthday)

    username = discord.ui.TextInput(
        label='Discord username',
        placeholder='user123',
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.b_day_service.delete_process(
            interaction=interaction,
            username=self.username.value,
        )
