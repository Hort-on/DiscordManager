from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.navigator_context import NavigationContext
from core.navigator.params_containers import AdminMenuParams
from core.navigator.routes import Route

from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_admins.superusers.formatter import SuperusersFormatter
    from features.for_admins.superusers.services import SuperusersService
    from features.for_admins.superusers.flow import SuperusersFlow
    from ui.button_protection.button_protection_service import ButtonProtectionService


class SuperusersMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            formatter: SuperusersFormatter,
            superusers_service: SuperusersService,
            buttons_protection: ButtonProtectionService
    ):
        super().__init__(
            label='👮Superusers management',
            style=discord.ButtonStyle.secondary,
            service=buttons_protection
        )
        self.navigator = navigator
        self.formatter = formatter
        self.superusers_service = superusers_service

    async def on_click(self, interaction: discord.Interaction) -> None:
        view = self.navigator.superusers_menu()

        context = getattr(view, 'context', None)
        if context is None:
            context = NavigationContext()
            view.context = context

        context.push(target=Route.ADMIN_MENU,
                     params=AdminMenuParams(
                         guild_id=interaction.guild_id
                     ))

        embed = self.formatter.build_embed(guild=interaction.guild)

        await interaction.response.edit_message(view=view, embed=embed)


class AddSuperuserButton(FirewallButton):
    scope = 'admin'

    def __init__(self, buttons_protection: ButtonProtectionService, flow: SuperusersFlow):
        super().__init__(
            label='📥Add super user',
            style=discord.ButtonStyle.green,
            service=buttons_protection
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.start_for_add(interaction=interaction)


class DeleteSuperusersButton(FirewallButton):
    scope = 'admin'

    def __init__(self, buttons_protection: ButtonProtectionService, flow: SuperusersFlow):
        super().__init__(
            label='🗑️Delete superusers',
            style=discord.ButtonStyle.red,
            service=buttons_protection
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction):
        await self.flow.start_for_delete(interaction=interaction)


class SuperusersListButton(FirewallButton):
    scope = 'admin'

    def __init__(self, buttons_protection: ButtonProtectionService, flow: SuperusersFlow):
        super().__init__(
            label='📑Show current superusers',
            style=discord.ButtonStyle.blurple,
            service=buttons_protection
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction):
        await self.flow.for_superusers_list(interaction=interaction)
