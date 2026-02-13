from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.navigator import Navigator

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton

from core.navigator_context import NavigationContext


class RoleManagerMenuButton(FirewallButton):
    scope = 'user'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Role manager',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        params_main = {
            'guild': interaction.guild,
            'user_id': interaction.user.id
        }

        context.push(target='main_menu', params=params_main)

        view = self.navigator.go(target='role_manager_menu')

        view.context = context

        await interaction.response.edit_message(view=view)
