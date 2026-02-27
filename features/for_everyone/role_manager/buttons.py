from __future__ import annotations

from typing import TYPE_CHECKING

import discord.ui

from core.navigator.navigator_context import NavigationContext
from core.navigator.params_containers import MainMenuParams
from core.navigator.routes import Route


if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_everyone.role_manager.flow import RoleManagerFlow


class RoleManagerMenuButton(discord.ui.Button):
    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Role manager',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        view = self.navigator.role_manager_menu()

        context = getattr(view, 'context', None)
        if context is None:
            context = NavigationContext()
            view.context = context

        context.push(target=Route.MAIN_MENU,
                     params=MainMenuParams(
                         guild_id=interaction.guild_id,
                         user_id=interaction.user.id,
                         owner_id=interaction.guild.owner_id
                     ))

        await interaction.response.edit_message(view=view)


class AddRoleButton(discord.ui.Button):
    def __init__(self, navigator: Navigator, flow: RoleManagerFlow):
        super().__init__(
            label='Add role',
            style=discord.ButtonStyle.green
        )
        self.navigator = navigator
        self.flow = flow

    async def callback(self, interaction: discord.Interaction) -> None:
        await self.flow.start_for_add(interaction=interaction)


class RemoveRoleButton(discord.ui.Button):
    def __init__(self, navigator: Navigator, flow: RoleManagerFlow):
        super().__init__(
            label='Remove role',
            style=discord.ButtonStyle.red
        )
        self.navigator = navigator
        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.start_for_remove(interaction=interaction)
