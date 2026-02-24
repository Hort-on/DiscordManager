import discord

from modules.buttons.for_admins.birthday_buttons.services import AddBirthdayService, DeleteBirthdayService


class AddBirthdayModal(discord.ui.Modal, title='Please enter a birthday:'):
    def __init__(self):
        super().__init__()
        self.add_birthday = AddBirthdayService()

    username = discord.ui.TextInput(
        label='Discord username',
        placeholder='user123',
        required=True
    )

    birthday_input = discord.ui.TextInput(
        label='Birthday (DD.MM)',
        placeholder='31.12',
        required=True,
        min_length=5,
        max_length=5
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.add_birthday.add_process(
            interaction=interaction,
            username=self.username.value,
            birthday=self.birthday_input.value
        )


class DeleteBirthdayModal(discord.ui.Modal, title='Delete birthday'):
    def __init__(self):
        super().__init__()
        self.del_birthday = DeleteBirthdayService()

    username = discord.ui.TextInput(
        label='Discord username',
        placeholder='user123',
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.del_birthday.delete_process(
            interaction=interaction,
            username=self.username.value,
        )
