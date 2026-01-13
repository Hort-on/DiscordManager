import discord.ui

from services.buttons.protection.admin_buttons_protection import FirewallButton
from services.modals.superuser_modal.add_superusers import AddSuperusersModal


class AddSUserButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Add super user',
            style=discord.ButtonStyle.green
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()

        await interaction.response.send_modal(AddSuperusersModal())
