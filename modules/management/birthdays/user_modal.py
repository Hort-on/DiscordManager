import discord

from modules.buttons.for_admins.birthday_buttons.services import AddBirthdayService


class UserBirthdayModal(discord.ui.Modal, title='Please add your birthday:'):
    def __init__(self):
        super().__init__()
        self.add_birthday = AddBirthdayService()

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
            username=interaction.user.global_name,
            birthday=self.birthday_input.value
        )
