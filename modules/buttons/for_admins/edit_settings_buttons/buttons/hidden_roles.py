from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator

import discord

from database.settings_storage.settings_manager import StorageTarget

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.buttons.for_admins.edit_settings_buttons.services.hidden_roles_service import HiddenRolesService
from modules.buttons.for_admins.edit_settings_buttons.services.settings_formatter import SettingsFormatter

from services.buttons.navigator_context import NavigationContext
from services.drop_down_menu.drop_down_selector import DropMenuView
from services.embed_constructor.embed_constructor import ErrorEmbed


class HiddenRolesMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Hidden roles management',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='settings_menu')

        view = self.navigator.go(target='hidden_roles_menu')

        view.context = context

        await interaction.response.edit_message(view=view)


class AddHiddenRoleButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='📥Add hidden roles',
            style=discord.ButtonStyle.green
        )
        self.service = HiddenRolesService(navigator=navigator)
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='hidden_roles_menu')

        formatter = SettingsFormatter()
        embed = await formatter.format_current_hidden_roles(interaction)

        options = self.service.for_add_roles_options(
            guild=interaction.guild
        )

        if not options:
            embed = ErrorEmbed(
                description='No available roles to be add.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the roles you want to add',
            callback=self.service.for_add_role_save,
            max_values=min(25, len(options))
        )

        view.context = context

        await interaction.response.edit_message(
            view=view,
            embed=embed
        )


class DeleteHiddenRoleButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='🗑️Delete hidden roles',
            style=discord.ButtonStyle.red,
        )
        self.service = HiddenRolesService(navigator=navigator)
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='hidden_roles_menu')

        formatter = SettingsFormatter()
        embed = await formatter.format_current_hidden_roles(interaction)

        options = self.service.for_remove_roles_options(
            guild=interaction.guild,
            target=StorageTarget.HIDDEN_ROLES
        )

        if not options:
            embed = ErrorEmbed(
                description='No hidden roles were added.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the roles you want to delete',
            callback=self.service.for_remove_role_data,
            max_values=min(25, len(options))
        )

        view.context = context

        await interaction.response.edit_message(
            view=view,
            embed=embed
        )


class HiddenRolesListButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='📄Hidden roles list',
            style=discord.ButtonStyle.blurple,
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        formatter = SettingsFormatter()
        embed = await formatter.format_current_hidden_roles(interaction)

        await interaction.response.edit_message(
            embed=embed
        )
