from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator_context import NavigationContext

from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator import Navigator
    from features.for_admins.superusers.formatter import SuperusersFormatter


class SuperusersMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            formatter: SuperusersFormatter
    ):
        super().__init__(
            label='👮Superusers management',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator
        self.formatter = formatter

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='admin_menu', params={'guild_id': interaction.guild_id})

        view = self.navigator.go(target='superusers_menu')

        view.context = context

        embed = self.formatter.build_embed(guild=interaction.guild)

        await interaction.response.edit_message(view=view, embed=embed)
