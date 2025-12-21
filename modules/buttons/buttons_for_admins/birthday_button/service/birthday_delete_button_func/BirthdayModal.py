import discord

from .BirthdayService import DeleteBirthdayService


class DeleteBirthdayModal(discord.ui.Modal, title='Delete birthday'):
    username = discord.ui.TextInput(
        label='Discord username',
        placeholder='user123',
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await DeleteBirthdayService.process(
            interaction=interaction,
            username=self.username.value,
        )
