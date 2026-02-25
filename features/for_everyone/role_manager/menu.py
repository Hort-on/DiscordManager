from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.routes import Route
from core.navigator.navigator_context import NavigationContext

from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator


class RoleManagerMenuButton(FirewallButton):
    scope = 'user'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Role manager',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        params_main = {
            'guild': interaction.guild,
            'user_id': interaction.user.id
        }

        view = self.navigator.go(target=Route.ROLE_MANAGER_MENU)

        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='main_menu', params=params_main)

        view.context = context

        await interaction.response.edit_message(view=view)
