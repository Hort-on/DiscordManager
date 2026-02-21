from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator_context import NavigationContext

from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator import Navigator


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
