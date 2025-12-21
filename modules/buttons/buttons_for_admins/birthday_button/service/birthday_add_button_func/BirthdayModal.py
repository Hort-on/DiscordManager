import discord

from .BirthdayService import AddBirthdayService


class AddBirthdayModal(discord.ui.Modal, title='Please enter a birthday:'):
    username = discord.ui.TextInput(
        label='Discord username',
        placeholder='user123',
        required=True
    )

    birthday = discord.ui.TextInput(
        label='Birthday (DD.MM)',
        placeholder='31.12',
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await AddBirthdayService.process(
            interaction=interaction,
            username=self.username.value,
            birthday=self.birthday.value
        )
