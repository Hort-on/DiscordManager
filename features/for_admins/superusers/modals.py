import discord

from modules.buttons.for_admins.superusers_buttons.services import AddSuperusersService


class AddSuperusersModal(discord.ui.Modal, title='Superuser names.'):
    def __init__(self):
        super().__init__()
        self.superuser_procedure = AddSuperusersService()

    superuser_names = discord.ui.TextInput(
        label='Please type superuser names',
        placeholder='user123, user456, user_, _user, etc.',
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.superuser_procedure.superuser_proceed(
            interaction=interaction,
            superuser_names=self.superuser_names.value
        )
