from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from services.buttons.navigator import Navigator

import discord

from database.settings_storage.settings_manager import StorageTarget

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.buttons.for_admins.edit_settings_buttons.settings_formatter import SettingsFormatter
from modules.buttons.other_buttons.back import BackButton
from modules.buttons.for_admins.edit_settings_buttons.services.hidden_service import HiddenService

from services.buttons.navigator_context import NavigationContext
from services.drop_down_menu.drop_down_selector import DropMenuView
from services.embed_constructor.embed_constructor import ErrorEmbed


class HiddenChannelsManagement(FirewallButton):
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

        view = HiddenChMenuView(navigator=self.navigator)

        view.context = context

        await interaction.response.edit_message(view=view)


class AddHiddenChannel(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='📥Add hidden channels',
            style=discord.ButtonStyle.green
        )
        self.service = HiddenService(navigator=navigator)
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='Hidden_ch_menu')

        formatter = SettingsFormatter()
        embed = await formatter.format_current_hidden_channels(interaction)

        options = self.service.for_add_build_options(
            guild_id=interaction.guild_id,
            target=StorageTarget.HIDDEN_CHANNELS,
            storage=interaction.guild.channels
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
            callback=self.service.for_add_ch_save,
            max_values=min(25, len(options))
        )

        view.context = context

        await interaction.response.edit_message(
            view=view,
            embed=embed
        )


class DeleteHiddenChannel(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='🗑️Delete hidden channels',
            style=discord.ButtonStyle.red
        )
        self.service = HiddenService(navigator=navigator)
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        context = getattr(self.view, 'context', NavigationContext())

        context.push(target='Hidden_ch_menu')

        formatter = SettingsFormatter()
        embed = await formatter.format_current_hidden_channels(interaction)

        options = self.service.for_delete_build_options(
            guild=interaction.guild,
            target=StorageTarget.HIDDEN_CHANNELS
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
            callback=self.service.for_remove_ch_data,
            max_values=min(25, len(options))
        )

        view.context = context

        await interaction.response.edit_message(
            view=view,
            embed=embed
        )


class HiddenChMenuView(discord.ui.View):
    def __init__(self, navigator: Navigator):
        super().__init__(timeout=60)

        self.add_item(AddHiddenChannel(navigator=navigator))
        self.add_item(DeleteHiddenChannel(navigator=navigator))
        self.add_item(BackButton(navigator=navigator))
