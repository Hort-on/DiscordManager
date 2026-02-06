from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton

from services.buttons.navigator_context import NavigationContext


class EditSettingsMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='⚙️ Settings management',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction):
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='admin_menu', params={'guild_id': interaction.guild_id})

        view = self.navigator.go(target='settings_menu')

        view.context = context

        await interaction.response.edit_message(
            content='⚙️ Settings management',
            view=view
        )
