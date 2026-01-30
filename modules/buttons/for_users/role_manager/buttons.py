from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator

import discord.ui

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.buttons.for_users.role_manager.services import AddRoleService, RemoveRoleService


class AddRoleButton(FirewallButton):
    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Add role',
            style=discord.ButtonStyle.green
        )
        self.add_role = AddRoleService(navigator=navigator)

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.add_role.prepare_roles(interaction=interaction)


class RemoveRoleButton(FirewallButton):
    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Remove role',
            style=discord.ButtonStyle.red
        )
        self.remove_role = RemoveRoleService(navigator=navigator)

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.remove_role.prepare_roles(interaction=interaction)
