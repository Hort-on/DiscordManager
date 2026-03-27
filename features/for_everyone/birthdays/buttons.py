from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.params_containers import MainMenuParams
from core.navigator.routes import Route

from features.for_everyone.birthdays.flow import BirthdayFlow

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from features.for_everyone.birthdays.service import BirthdayService
    from general_services.translator.translator import Translator


class BirthdayMenuButton(discord.ui.Button):
    def __init__(
            self,
            navigator: Navigator,
            context: NavigationContext,
            service: BirthdayService,
            translator: Translator,
            guild_id: int
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='BIRTHDAYS',
                key='birthdays'
            ),
            style=discord.ButtonStyle.secondary
        )

        self.navigator = navigator
        self.context = context
        self.service = service
        self.translator = translator

    async def callback(self, interaction: discord.Interaction):
        view = self.navigator.birthday_menu(guild_id=interaction.guild_id)

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


class AddBirthdayButton(discord.ui.Button):
    def __init__(self, flow: BirthdayFlow, translator: Translator, guild_id: int):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='BIRTHDAYS',
                key='add_birthday'
            ),
            style=discord.ButtonStyle.blurple
        )

        self.flow = flow

    async def callback(self, interaction: discord.Interaction) -> None:
        await self.flow.for_add_button(interaction=interaction)


class DeleteBirthdayButton(discord.ui.Button):
    def __init__(self, flow: BirthdayFlow, translator: Translator, guild_id: int):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='BIRTHDAYS',
                key='del_birthday'
            ),
            style=discord.ButtonStyle.red
        )

        self.flow = flow

    async def callback(self, interaction: discord.Interaction):
        await self.flow.for_delete_button(interaction=interaction)
