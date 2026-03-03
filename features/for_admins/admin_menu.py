from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.routes import Route
from core.navigator.params_containers import MainMenuParams
from core.navigator.navigator_context import NavigationContext

from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from ui.button_protection.button_protection_service import ButtonProtectionService


class AdminMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator, buttons_protection: ButtonProtectionService, context: NavigationContext):
        super().__init__(
            label='🛠️Admin menu',
            style=discord.ButtonStyle.secondary,
            protection_service=buttons_protection
        )

        self.navigator = navigator
        self.context = context

    async def on_click(self, interaction: discord.Interaction):
        view = self.navigator.admin_menu(
            guild_id=interaction.guild_id,
            context=self.context
        )

        view.context = self.context

        self.context.push(
            target=Route.MAIN_MENU,
            params=MainMenuParams(
                guild_id=interaction.guild_id,
                user_id=interaction.user.id,
                owner_id=interaction.guild.owner_id
            )
        )

        await interaction.response.edit_message(view=view)
