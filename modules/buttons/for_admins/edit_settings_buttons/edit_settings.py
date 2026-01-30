from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.buttons.for_admins.edit_settings_buttons.settings_formatter import SettingsFormatter
from modules.buttons.for_admins.edit_settings_buttons.service import ToggleService

from services.buttons.navigator_context import NavigationContext
from services.drop_down_menu.drop_down_selector import DropMenuView


class EditSettingsButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Edit settings',
            style=discord.ButtonStyle.green
        )
        self.service = ToggleService(navigator=navigator)
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='admin_menu', params={'guild_id': interaction.guild_id})

        formatter = SettingsFormatter()
        embed = await formatter.format_settings(interaction)

        options = self.service.prepare_options()

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the module you want to change',
            callback=self.service.proceed
        )

        view.context = context

        await interaction.response.edit_message(
            view=view,
            embed=embed
        )
