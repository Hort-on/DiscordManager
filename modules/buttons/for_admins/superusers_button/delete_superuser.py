import discord

from services.buttons.for_admins.superusers.delete_superuser_service import DeleteSuperuserService
from services.buttons.protection.admin_buttons_protection import FirewallButton


class DeleteSuperusersButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Show current superusers',
            style=discord.ButtonStyle.green,
        )

    async def on_click(self, interaction: discord.Interaction):
        service = DeleteSuperuserService()
        await service.prepare_users(interaction=interaction)
