import discord

from modules.configuration.superuser_service.superuser_service import SuperUserService


class SuperUserModal(discord.ui.Modal, title='Superuser names.'):
    def __init__(self, parent):
        super().__init__()
        self.superuser_procedure = SuperUserService()

    superuser_names = discord.ui.TextInput(
        label='Please provide superuser names',
        placeholder='user123, user456, user_, _user, etc.',
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.superuser_procedure.superuser_proceed(
            interaction=interaction,
            superuser_names=self.superuser_names.value
        )
