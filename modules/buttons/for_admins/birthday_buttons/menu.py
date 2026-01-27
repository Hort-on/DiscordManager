from __future__ import annotations

import discord

from services.buttons.navigator_context import NavigationContext

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator


class BirthdayMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='🎂 Birthdays',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction):
        context = NavigationContext()

        context.back_view(target='admin_menu', params={'guild_id': interaction.guild_id})

        view = self.navigator.go(target='birthday_menu')

        await interaction.response.edit_message(
            content='🎂 Birthday management',
            view=view
        )
