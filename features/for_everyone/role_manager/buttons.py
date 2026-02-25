from __future__ import annotations

from typing import TYPE_CHECKING

import discord.ui

from core.navigator.navigator_context import NavigationContext
from core.navigator.routes import Route

from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.embed_constructor.embed_constructor import ErrorEmbed

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_everyone.role_manager.services import RoleManagerService
    from features.for_everyone.role_manager.flow import RoleManagerFlow


class AddRoleButton(discord.ui.Button):
    def __init__(self, navigator: Navigator, service: RoleManagerService, flow: RoleManagerFlow):
        super().__init__(
            label='Add role',
            style=discord.ButtonStyle.green
        )
        self.navigator = navigator
        self.service = service

    async def callback(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target=Route.ROLE_MANAGER_MENU)

        options = await self.service.prepare_roles(interaction=interaction)

        if not options:
            embed = ErrorEmbed(
                description='No available roles were found.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please choose the roles you want to add:',
            callback=self.add_role.add_role_to_user,
            max_values=min(25, len(options))
        )

        view.context = context

        await interaction.response.edit_message(view=view)


class RemoveRoleButton(discord.ui.Button):
    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Remove role',
            style=discord.ButtonStyle.red
        )
        self.navigator = navigator
        self.remove_role = RemoveRoleService(navigator=navigator)

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='role_manager_menu')

        options = await self.remove_role.prepare_roles(interaction=interaction)

        if not options:
            embed = ErrorEmbed(
                description='No roles available to remove were found.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please choose the roles you want to remove:',
            callback=self.remove_role.remove_role_from_user,
            max_values=min(25, len(options))
        )

        view.context = context

        await interaction.response.edit_message(view=view)
