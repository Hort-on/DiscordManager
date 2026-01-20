import discord.ui

from modules.buttons.for_users.role_manager.services import AddRoleService, RemoveRoleService
from modules.buttons.services.protection.admin_buttons_protection import FirewallButton


class AddRoleButton(FirewallButton):
    def __init__(self):
        super().__init__(
            label='Add role',
            style=discord.ButtonStyle.green
        )
        self.add_role = AddRoleService()

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.add_role.prepare_roles(interaction=interaction)


class RemoveRoleButton(FirewallButton):
    def __init__(self):
        super().__init__(
            label='Remove role',
            style=discord.ButtonStyle.red
        )
        self.remove_role = RemoveRoleService()

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.remove_role.prepare_roles(interaction=interaction)
