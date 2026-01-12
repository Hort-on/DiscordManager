import discord.ui

from services.modals.superuser_modal.add_superusers import AddSuperusersModal


class AddSUserButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Add super user',
            style = discord.ButtonStyle.green
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()

        await interaction.response.send_modal(AddSuperusersModal())
