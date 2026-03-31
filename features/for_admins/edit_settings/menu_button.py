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
    from general_services.translator.translator import Translator


class EditSettingsMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            context: NavigationContext,
            buttons_protection: ButtonProtectionService,
            translator: Translator,
            guild_id: int
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='EDIT_SETTINGS',
                key='settings_menu'
            ),
            style=discord.ButtonStyle.secondary,
            protection_service=buttons_protection
        )

        self.navigator = navigator
        self.context = context
        self.translator = translator

    async def on_click(self, interaction: discord.Interaction):
        guild = interaction.guild
        assert guild is not None

        view = self.navigator.settings_menu(
            context=self.context,
            guild_id=guild.id
        )

        view.context = self.context
        self.context.push(
            target=Route.ADMIN_MENU,
            params=AdminMenuParams(guild_id=guild.id)
        )

        await interaction.response.edit_message(view=view)
