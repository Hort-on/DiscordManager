from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.buttons.for_admins.edit_settings_buttons.services.settings_formatter import SettingsFormatter
from modules.buttons.for_admins.edit_settings_buttons.services.hidden_channels_service import HiddenChannelsService

from services.buttons.navigator_context import NavigationContext
from services.drop_down_menu.drop_down_selector import DropMenuView
from services.embed_constructor.embed_constructor import ErrorEmbed


class HiddenChannelsMenuButtons(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Hidden channels management',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='settings_menu')

        view = self.navigator.go(target='hidden_channels_menu')

        view.context = context

        await interaction.response.edit_message(view=view)


class AddHiddenChannelButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='📥Add hidden channels',
            style=discord.ButtonStyle.green
        )
        self.service = HiddenChannelsService(navigator=navigator)
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='hidden_channels_menu')

        formatter = SettingsFormatter()
        embed = await formatter.format_current_hidden_channels(interaction)

        options = self.service.for_add_channel_options(
            guild=interaction.guild
        )

        if not options:
            embed = ErrorEmbed(
                description='No available channels to be add.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the module you want to change',
            callback=self.service.for_add_channel_save,
            max_values=min(25, len(options))
        )

        view.context = context

        await interaction.response.edit_message(
            view=view,
            embed=embed
        )


class DeleteHiddenChannelButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='🗑️Delete hidden channels',
            style=discord.ButtonStyle.red
        )
        self.service = HiddenChannelsService(navigator=navigator)
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='hidden_channels_menu')

        formatter = SettingsFormatter()
        embed = await formatter.format_current_hidden_channels(interaction)

        options = self.service.for_remove_channel_options(
            guild=interaction.guild,
        )

        if not options:
            embed = ErrorEmbed(
                description='No hidden channels were added.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the channel you want to delete',
            callback=self.service.for_remove_channel_data,
            max_values=min(25, len(options))
        )

        view.context = context

        await interaction.response.edit_message(
            view=view,
            embed=embed
        )


class HiddenChannelsListButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='📄Hidden channels list',
            style=discord.ButtonStyle.blurple
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        formatter = SettingsFormatter()
        embed = await formatter.format_current_hidden_channels(interaction)

        await interaction.response.edit_message(embed=embed)
