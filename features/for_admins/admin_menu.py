from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.navigator_context import NavigationContext
from core.navigator.params_containers import MainMenuParams
from core.navigator.routes import Route
from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from general_services.translator.translator import Translator
    from ui.button_protection.button_protection_service import ButtonProtectionService


class AdminMenuButton(FirewallButton):
    scope = "admin"

    def __init__(
        self,
        navigator: Navigator,
        buttons_protection: ButtonProtectionService,
        context: NavigationContext,
        translator: Translator,
        guild_id: int,
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id, section="SYSTEM_GENERAL", key="admin_menu"
            ),
            style=discord.ButtonStyle.secondary,
            protection_service=buttons_protection,
        )

        self.navigator = navigator
        self.context = context

    async def on_click(self, interaction: discord.Interaction):
        guild = interaction.guild
        assert guild is not None

        view = self.navigator.admin_menu(guild_id=guild.id, context=self.context)

        view.context = self.context

        self.context.push(
            target=Route.MAIN_MENU,
            params=MainMenuParams(
                guild_id=guild.id, user_id=interaction.user.id, owner_id=guild.owner_id
            ),
        )

        await interaction.response.edit_message(view=view)
