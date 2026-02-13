from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.navigator import Navigator

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.buttons.for_admins.superusers_buttons.modals import AddSuperusersModal
from modules.buttons.for_admins.superusers_buttons.format_users_list import SuperusersFormatter
from modules.buttons.for_admins.superusers_buttons.services import DeleteSuperuserService

from core.navigator_context import NavigationContext
from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.embed_constructor.embed_constructor import ErrorEmbed


class AddSuperuserButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='📥Add super user',
            style=discord.ButtonStyle.green
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(AddSuperusersModal())


class DeleteSuperusersButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='🗑️Delete superusers',
            style=discord.ButtonStyle.red,
        )
        self.navigator = navigator
        self.del_superuser = DeleteSuperuserService(navigator=navigator)

    async def on_click(self, interaction: discord.Interaction):
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='superusers_menu')

        options = await self.del_superuser.prepare_users(interaction=interaction)

        if not options:
            embed = ErrorEmbed(
                description='No superusers were assigned yet'
            )
            await interaction.response.edit_message(embed=embed)
            return

        formatter = SuperusersFormatter()

        embed = formatter.build_embed(interaction=interaction)

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please choose the users you want to delete:',
            callback=self.del_superuser.delete_superuser_callback,
            max_values=min(25, len(options))
        )

        view.context = context

        await interaction.response.edit_message(
            embed=embed,
            view=view
        )


class SuperusersListButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='📑Show current superusers',
            style=discord.ButtonStyle.blurple,
        )
        self.superusers_list = SuperusersFormatter()

    async def on_click(self, interaction: discord.Interaction):
        embed = self.superusers_list.build_embed(interaction=interaction)
        await interaction.response.edit_message(embed=embed)
