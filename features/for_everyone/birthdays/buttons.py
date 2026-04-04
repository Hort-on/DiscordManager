from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.params_containers import MainMenuParams
from core.navigator.routes import Route

from features.for_everyone.birthdays.flow import BirthdayFlow

from ui.button_protection.admin_buttons_protection import FirewallButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from features.for_everyone.birthdays.service import BirthdayService
    from general_services.translator.translator import Translator
    from ui.button_protection.button_protection_service import ButtonProtectionService


class BirthdayMenuButton(discord.ui.Button):
    def __init__(
            self,
            navigator: Navigator,
            context: NavigationContext,
            service: BirthdayService,
            translator: Translator,
            admins: set[int],
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
        self.admins = admins

    async def callback(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        assert guild is not None

        view = self.navigator.birthday_menu(
            guild_id=guild.id,
            user_id=interaction.user.id,
            owner_id=guild.owner_id,
            admins=self.admins
        )

        view.context = self.context

        self.context.push(
            target=Route.MAIN_MENU,
            params=MainMenuParams(
                guild_id=guild.id,
                user_id=interaction.user.id,
                owner_id=guild.owner_id
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
            style=discord.ButtonStyle.green
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

    async def callback(self, interaction: discord.Interaction) -> None:
        await self.flow.for_delete_button(interaction=interaction)


class AddForAdmins(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            flow: BirthdayFlow,
            translator: Translator,
            guild_id: int,
            protection_service: ButtonProtectionService
    ):
        self.flow = flow

        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='BIRTHDAYS',
                key='for_admin_add'
            ),
            style=discord.ButtonStyle.blurple,
            protection_service=protection_service
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        await self.flow.add_for_admin(interaction=interaction)


class DeleteForAdmins(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            flow: BirthdayFlow,
            translator: Translator,
            guild_id: int,
            protection_service: ButtonProtectionService
    ):
        self.flow = flow

        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='BIRTHDAYS',
                key='for_admin_delete'
            ),
            style=discord.ButtonStyle.blurple,
            protection_service=protection_service
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        await self.flow.delete_for_admin(interaction=interaction)
