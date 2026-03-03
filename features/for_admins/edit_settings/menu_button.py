from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.params_containers import AdminMenuParams
from core.navigator.routes import Route

from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from ui.button_protection.button_protection_service import ButtonProtectionService


class EditSettingsMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            context: NavigationContext,
            buttons_protection: ButtonProtectionService,
    ):
        super().__init__(
            label='⚙️ Settings management',
            style=discord.ButtonStyle.secondary,
            protection_service=buttons_protection
        )

        self.navigator = navigator
        self.context = context

    async def on_click(self, interaction: discord.Interaction):
        view = self.navigator.settings_menu(context=self.context)

        view.context = self.context
        self.context.push(
            target=Route.ADMIN_MENU,
            params=AdminMenuParams(
                guild_id=interaction.guild_id
            )
        )

        await interaction.response.edit_message(
            content='⚙️ Settings management',
            view=view
        )
