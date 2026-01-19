import discord

from modules.buttons.for_admins.birthday_buttons.modals import AddBirthdayModal, DeleteBirthdayModal
from modules.buttons.services.protection.admin_buttons_protection import FirewallButton


class AddBirthdayButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Add birthday',
            style=discord.ButtonStyle.blurple
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(AddBirthdayModal())


class DeleteBirthdayButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Delete birthday',
            style=discord.ButtonStyle.red
        )

    async def on_click(self, interaction: discord.Interaction):
        await interaction.response.send_modal(DeleteBirthdayModal())
