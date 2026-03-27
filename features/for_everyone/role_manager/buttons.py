from __future__ import annotations

from typing import TYPE_CHECKING

import discord.ui

from core.navigator.params_containers import MainMenuParams
from core.navigator.routes import Route

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from features.for_everyone.role_manager.flow import RoleManagerFlow
    from general_services.translator.translator import Translator


class RoleManagerMenuButton(discord.ui.Button):
    def __init__(self, navigator: Navigator, context: NavigationContext, translator: Translator, guild_id: int):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='ROLE_MANAGER',
                key='role_manager'
            ),
            style=discord.ButtonStyle.secondary
        )

        self.navigator = navigator
        self.context = context

    async def callback(self, interaction: discord.Interaction) -> None:
        view = self.navigator.role_manager_menu(
            context=self.context,
            guild_id=interaction.guild_id
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


class AddRoleButton(discord.ui.Button):
    def __init__(self, navigator: Navigator, flow: RoleManagerFlow, translator: Translator, guild_id: int):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='ROLE_MANAGER',
                key='add_role'
            ),
            style=discord.ButtonStyle.green
        )
        self.navigator = navigator
        self.flow = flow

    async def callback(self, interaction: discord.Interaction) -> None:
        await self.flow.start_for_add(interaction=interaction)


class RemoveRoleButton(discord.ui.Button):
    def __init__(self, navigator: Navigator, flow: RoleManagerFlow, translator: Translator, guild_id: int):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='ROLE_MANAGER',
                key='remove_role'
            ),
            style=discord.ButtonStyle.red
        )
        self.navigator = navigator
        self.flow = flow

    async def on_click(self, interaction: discord.Interaction) -> None:
        await self.flow.start_for_remove(interaction=interaction)
