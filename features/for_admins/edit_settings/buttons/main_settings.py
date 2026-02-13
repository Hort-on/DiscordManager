from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.navigator import Navigator
    from features.for_admins.edit_settings.services.main_settings import EditMainSettingsService
    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter

import discord

from core.navigator_context import NavigationContext

from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.button_protection.admin_buttons_protection import FirewallButton


class MainSettingsButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            navigator: Navigator,
            service: EditMainSettingsService,
            formatter: SettingsFormatter
    ):
        super().__init__(
            label='Edit main settings',
            style=discord.ButtonStyle.green
        )
        self.service = service
        self.navigator = navigator
        self.formatter = formatter

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='settings_menu')

        embed = self.formatter.format_current_main_settings(interaction)

        options = self.service.build_options(guild_id=interaction.guild_id)

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the module you want to change.',
            callback=self.service.proceed_result
        )

        view.context = context

        await interaction.response.edit_message(
            view=view,
            embed=embed
        )
