import discord.ui

from services.buttons.protection.admin_buttons_protection import FirewallButton
from services.modals.superuser_modal.add_superusers import AddSuperusersModal


class AddSuperuserButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Add super user',
            style=discord.ButtonStyle.green
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(AddSuperusersModal())
