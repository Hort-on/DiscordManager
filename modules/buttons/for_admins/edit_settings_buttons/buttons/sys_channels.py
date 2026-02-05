from __future__ import annotations

from typing import TYPE_CHECKING

from services.drop_down_menu.drop_down_selector import DropMenuView
from services.embed_constructor.embed_constructor import ErrorEmbed

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.buttons.for_admins.edit_settings_buttons.services.system_channels import SystemChannelsService

from services.buttons.navigator_context import NavigationContext


class SystemChannelsManagement(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='📥system channels management',
            style=discord.ButtonStyle.blurple
        )
        self.service = SystemChannelsService(navigator=navigator)
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='settings_menu')

        options = self.service.build_options(guild_id=interaction.guild_id)

        if not options:
            embed = ErrorEmbed(
                description='No available channels found.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the channel you want to change',
            callback=self.service.choosing_the_channel
        )

        view.context = context

        embed = self.service.channel_list(guild_id=interaction.guild_id)

        await interaction.response.edit_message(embed=embed, view=view)
