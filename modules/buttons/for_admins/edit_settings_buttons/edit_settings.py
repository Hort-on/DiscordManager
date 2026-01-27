from __future__ import annotations

import discord

from core.container import AppContainer
from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.buttons.for_admins.edit_settings_buttons.services import SettingsFormatter

from services.buttons.navigator_context import NavigationContext

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator
    from core.container import BotContainer


class EditSettingsButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Edit settings',
            style=discord.ButtonStyle.green
        )
        self.container: BotContainer = AppContainer.get()
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = NavigationContext()

        context.back_view(target='admin_menu', params={'guild_id': interaction.guild_id})

        formatter = SettingsFormatter()
        embed = await formatter.format_settings(interaction)

        view = self.navigator.go(
            target='edit_settings',
            db_factory=self.container.db_factory,
            yes_no_factory=self.container.yes_no_factory,
        )

        view.context = context

        await interaction.response.edit_message(
            view=view,
            embed=embed
        )
