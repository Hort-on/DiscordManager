from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.routes import Route

from database.settings_storage.settings_manager import StorageTarget

from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed
from ui.drop_down_menu.drop_down_selector import DropMenuView

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext

    from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter
    from features.for_admins.edit_settings.services.hidden_channels import HiddenChannelsService

    from general_services.other_services.cleanup_service import CleanUpService


class HiddenChannelsFlow:
    def __init__(
            self,
            navigator: Navigator,
            context: NavigationContext,
            formatter: SettingsFormatter,
            hidden_ch_service: HiddenChannelsService,
            cleanup_service: CleanUpService
    ):

        self.navigator = navigator
        self.context = context
        self.formatter = formatter
        self.hidden_ch_service = hidden_ch_service
        self.cleanup = cleanup_service

    # ================================= METHODS FOR ADD BUTTON =================================
    async def start_for_add(self, interaction: discord.Interaction) -> None:
        embed = await self.formatter.format_current_hidden(
            interaction=interaction,
            target=StorageTarget.HIDDEN_CHANNELS
        )

        options = self._get_available_channels(
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
            placeholder='Please select the channel you want to change:',
            callback=self._update_channels_procedure,
            max_values=min(25, len(options))
        )

        view.context = self.context

        self.context.push(target=Route.HIDDEN_CHANNELS_MENU)

        await interaction.response.edit_message(
            view=view,
            embed=embed
        )

    def _get_available_channels(self, guild: discord.Guild) -> list[discord.SelectOption]:
        hidden_channels = self.hidden_ch_service.get_hidden_channels(
            guild_id=guild.id
        )

        return [
            discord.SelectOption(
                label=channel.name,
                value=str(channel.id)
            )
            for channel in guild.channels if channel.id not in hidden_channels
        ]

    async def _update_channels_procedure(
            self,
            interaction: discord.Interaction,
            values: list[str],
    ):
        result = self.hidden_ch_service.update_channels_values(
            guild_id=interaction.guild_id,
            values=values,
        )

        if not result:
            error_embed = ErrorEmbed(
                description='Something went wrong, please try again later.'
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        await self._send_result(
            interaction=interaction,
            values=values
        )

    # ================================= METHODS FOR DELETE BUTTON =================================
    async def start_for_delete(self, interaction: discord.Interaction) -> None:
        embed = await self.formatter.format_current_hidden(
            interaction=interaction,
            target=StorageTarget.HIDDEN_CHANNELS
        )

        options = self._get_deletable_channels(
            guild=interaction.guild,
        )

        if not options:
            embed = ErrorEmbed(
                description='No available channels to be deleted.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the channel you want to delete:',
            callback=self._delete_channels_procedure,
            max_values=min(25, len(options))
        )

        view.context = self.context

        self.context.push(target=Route.HIDDEN_CHANNELS_MENU)

        await interaction.response.edit_message(
            view=view,
            embed=embed
        )

    def _get_deletable_channels(self, guild: discord.Guild) -> list[discord.SelectOption]:
        not_found_channels: set[int] = set()

        hidden_channels = self.hidden_ch_service.get_hidden_channels(
            guild_id=guild.id
        )

        available_channels: dict[int, str] = {}
        for channel_id in hidden_channels:
            channel = guild.get_channel(channel_id)

            if not channel:
                not_found_channels.add(channel_id)
                continue

            available_channels[channel_id] = channel.name

        if not_found_channels:
            self.cleanup.clean_up_hidden_channels(
                guild_id=guild.id,
                values=not_found_channels
            )

        return [
            discord.SelectOption(
                label=value,
                value=str(key)
            )
            for key, value in sorted(available_channels.items(), key=lambda i: i[0])
        ]

    async def _delete_channels_procedure(
            self,
            interaction: discord.Interaction,
            values: list[str],
    ) -> None:
        result = self.hidden_ch_service.delete_channels(
            guild_id=interaction.guild_id,
            values=values,
        )

        if not result:
            error_embed = ErrorEmbed(
                description='Something went wrong, please try again later.'
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        await self._send_result(
            interaction=interaction,
            values=values
        )

    # ================================= METHOD FOR SENDING RESULT =================================
    async def _send_result(self, interaction: discord.Interaction, values: list[str]) -> None:
        ch_ids = set(int(i) for i in values)

        ch_names: list[str] = ['These channels have been successfully added to hidden']

        for ch_id in ch_ids:
            channel = interaction.guild.get_channel(ch_id)
            ch_names.append(f'🔸 {channel.name}')

        result_msg = '\n'.join(ch_names)

        success_embed = SuccessEmbed(
            description=result_msg
        )

        settings_embed = await self.formatter.format_current_hidden(
            interaction=interaction,
            target=StorageTarget.HIDDEN_CHANNELS
        )

        await interaction.response.edit_message(
            embeds=[settings_embed, success_embed]
        )

    async def for_channels_list(self, interaction: discord.Interaction) -> None:
        embed = await self.formatter.format_current_hidden(
            interaction=interaction,
            target=StorageTarget.HIDDEN_CHANNELS
        )
        await interaction.response.edit_message(embed=embed)
