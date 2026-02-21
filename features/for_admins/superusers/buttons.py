from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.for_admins.superusers.flow import SuperusersFlow

from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator import Navigator
    from features.for_admins.superusers.formatter import SuperusersFormatter
    from features.for_admins.superusers.services import SuperusersService


class AddSuperuserButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            superusers_service: SuperusersService,
            formatter: SuperusersFormatter
    ):
        super().__init__(
            label='📥Add super user',
            style=discord.ButtonStyle.green
        )

        self.navigator = navigator
        self.superusers_service = superusers_service
        self.formatter = formatter

    async def on_click(self, interaction: discord.Interaction) -> None:
        flow = SuperusersFlow(
            navigator=self.navigator,
            superusers_service=self.superusers_service,
            formatter=self.formatter
        )

        await flow.start_for_add(
            interaction=interaction
        )


class DeleteSuperusersButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            superusers_service: SuperusersService,
            formatter: SuperusersFormatter
    ):
        super().__init__(
            label='🗑️Delete superusers',
            style=discord.ButtonStyle.red,
        )
        self.navigator = navigator
        self.superusers_service = superusers_service
        self.formatter = formatter

    async def on_click(self, interaction: discord.Interaction):
        flow = SuperusersFlow(
            navigator=self.navigator,
            superusers_service=self.superusers_service,
            formatter=self.formatter
        )

        await flow.start_for_delete(
            interaction=interaction
        )


class SuperusersListButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            formatter: SuperusersFormatter
    ):
        super().__init__(
            label='📑Show current superusers',
            style=discord.ButtonStyle.blurple,
        )
        self.formatter = formatter

    async def on_click(self, interaction: discord.Interaction):
        embed = self.formatter.build_embed(guild=interaction.guild)
        await interaction.response.edit_message(embed=embed)
