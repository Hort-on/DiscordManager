from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.buttons.for_admins.superusers_buttons.format_users_list import SuperusersFormatter

from services.buttons.navigator_context import NavigationContext


class SuperusersMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='👮Superusers management',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='admin_menu', params={'guild_id': interaction.guild_id})

        view = self.navigator.go(target='superusers_menu')

        view.context = context

        formatter = SuperusersFormatter()
        embed = formatter.build_embed(interaction=interaction)

        await interaction.response.edit_message(view=view, embed=embed)
