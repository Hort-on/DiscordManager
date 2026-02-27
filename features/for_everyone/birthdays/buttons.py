from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.params_containers import MainMenuParams
from core.navigator.routes import Route
from core.navigator.navigator_context import NavigationContext

from features.for_everyone.birthdays.flow import BirthdayFlow

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_everyone.birthdays.service import BirthdayService


class BirthdayMenuButton(discord.ui.Button):
    def __init__(self, navigator: Navigator, service: BirthdayService):
        super().__init__(
            label='🎂 Birthdays',
            style=discord.ButtonStyle.secondary
        )

        self.navigator = navigator
        self.service = service

    async def callback(self, interaction: discord.Interaction):
        view = self.navigator.birthday_menu()

        context = getattr(view, 'context', None)
        if context is None:
            context = NavigationContext()
            view.context = context

        context.push(target=Route.MAIN_MENU,
                     params=MainMenuParams(
                         guild_id=interaction.guild_id,
                         user_id=interaction.user.id,
                         owner_id=interaction.guild.owner_id
                     ))

        await interaction.response.edit_message(
            content='🎂 Birthday management',
            view=view
        )


class AddBirthdayButton(discord.ui.Button):
    def __init__(self, flow: BirthdayFlow):
        super().__init__(
            label='Add birthday',
            style=discord.ButtonStyle.blurple
        )

        self.flow = flow

    async def callback(self, interaction: discord.Interaction) -> None:
        await self.flow.for_add_button(interaction=interaction)


class DeleteBirthdayButton(discord.ui.Button):
    def __init__(self, flow: BirthdayFlow):
        super().__init__(
            label='Delete birthday',
            style=discord.ButtonStyle.red
        )

        self.flow = flow

    async def callback(self, interaction: discord.Interaction):
        await self.flow.for_delete_button(interaction=interaction)
