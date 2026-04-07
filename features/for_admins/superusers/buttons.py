from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.params_containers import AdminMenuParams
from core.navigator.routes import Route
from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from features.for_admins.superusers.flow import SuperusersFlow
    from features.for_admins.superusers.formatter import SuperusersFormatter
    from general_services.translator.translator import Translator
    from ui.button_protection.button_protection_service import ButtonProtectionService


class SuperusersMenuButton(FirewallButton):
    scope = "admin"

    def __init__(
        self,
        navigator: Navigator,
        context: NavigationContext,
        formatter: SuperusersFormatter,
        buttons_protection: ButtonProtectionService,
        translator: Translator,
        guild_id: int,
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id, section="SUPERUSERS", key="superusers_menu"
            ),
            style=discord.ButtonStyle.secondary,
            protection_service=buttons_protection,
        )

        self.navigator = navigator
        self.context = context
        self.formatter = formatter

    async def on_click(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        assert guild is not None

        view = self.navigator.superusers_menu(context=self.context, guild_id=guild.id)

        view.context = self.context
        self.context.push(
            target=Route.ADMIN_MENU, params=AdminMenuParams(guild_id=guild.id)
        )

        embed = self.formatter.build_embed(guild=guild)

        await interaction.response.edit_message(view=view, embed=embed)


class AddSuperuserButton(FirewallButton):
    scope = "admin"

    def __init__(
        self,
        buttons_protection: ButtonProtectionService,
        flow: SuperusersFlow,
        translator: Translator,
        guild_id: int,
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id, section="SUPERUSERS", key="add_superusers"
            ),
            style=discord.ButtonStyle.green,
            protection_service=buttons_protection,
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.start_for_add(interaction=interaction)


class DeleteSuperusersButton(FirewallButton):
    scope = "admin"

    def __init__(
        self,
        buttons_protection: ButtonProtectionService,
        flow: SuperusersFlow,
        translator: Translator,
        guild_id: int,
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id, section="SUPERUSERS", key="delete_superusers"
            ),
            style=discord.ButtonStyle.red,
            protection_service=buttons_protection,
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction):
        await self.flow.start_for_delete(interaction=interaction)


class SuperusersListButton(FirewallButton):
    scope = "admin"

    def __init__(
        self,
        buttons_protection: ButtonProtectionService,
        flow: SuperusersFlow,
        translator: Translator,
        guild_id: int,
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id, section="SUPERUSERS", key="superusers_list"
            ),
            style=discord.ButtonStyle.blurple,
            protection_service=buttons_protection,
        )

        self.flow = flow

    async def on_click(self, interaction: discord.Interaction):
        await self.flow.for_superusers_list(interaction=interaction)
