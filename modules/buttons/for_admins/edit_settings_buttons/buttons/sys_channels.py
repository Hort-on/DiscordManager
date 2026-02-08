from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.buttons.for_admins.edit_settings_buttons.services.settings_formatter import SettingsFormatter

from modules.buttons.for_admins.edit_settings_buttons.services.system_channels import (
    AddSystemChannelsService,
    DeleteSystemChannelsService,
    build_options
)

from services.buttons.navigator_context import NavigationContext
from services.drop_down_menu.drop_down_selector import DropMenuView
from services.embed_constructor.embed_constructor import ErrorEmbed


class SystemChannelsMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='System channels management',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='settings_menu')

        view = self.navigator.go(target='system_channels_menu')

        view.context = context

        await interaction.response.edit_message(view=view)


class AddSystemChannelsButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='📥Add\\Change channels',
            style=discord.ButtonStyle.green
        )
        self.service = AddSystemChannelsService(navigator=navigator)
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='system_channels_menu')

        options = build_options(guild_id=interaction.guild_id)

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

        formatter = SettingsFormatter()
        embed = await formatter.format_current_system_channels(guild=interaction.guild)

        await interaction.response.edit_message(embed=embed, view=view)


class DeleteSystemChannelsButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='🗑️Delete system channels',
            style=discord.ButtonStyle.red
        )
        self.service = DeleteSystemChannelsService(navigator=navigator)
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='system_channels_menu')

        options = build_options(guild_id=interaction.guild_id)

        if not options:
            embed = ErrorEmbed(
                description='No available channels found.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the channel you want to delete',
            callback=self.service.delete_channel,
            max_values=min(25, len(options))
        )

        view.context = context

        formatter = SettingsFormatter()
        embed = await formatter.format_current_system_channels(guild=interaction.guild)

        await interaction.response.edit_message(embed=embed, view=view)


class SystemChannelsListButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='📄System channels list',
            style=discord.ButtonStyle.blurple
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        formatter = SettingsFormatter()
        embed = await formatter.format_current_system_channels(guild=interaction.guild)

        await interaction.response.edit_message(embed=embed)
