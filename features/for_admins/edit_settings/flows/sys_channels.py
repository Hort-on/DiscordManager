from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.navigator_context import NavigationContext
from core.navigator.routes import Route

from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.embed_constructor.embed_constructor import SuccessEmbed, ErrorEmbed

from features.for_admins.edit_settings.services.system_channels import SystemChannelsService
from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator


class SystemChannelsFlow:
    def __init__(
            self,
            navigator: Navigator,
            sys_channels_service: SystemChannelsService,
            formatter: SettingsFormatter
    ):
        self.navigator = navigator
        self.service = sys_channels_service
        self.formatter = formatter

    # ================================= METHODS FOR ADD BUTTON =================================
    async def start_for_add(self, interaction: discord.Interaction) -> None:
        options = self._sys_channels_options(
            guild_id=interaction.guild_id
        )

        if not options:
            embed = ErrorEmbed(
                description='No available channels found.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select a system channel you want to change:',
            callback=self._select_new_sys_channel
        )

        context = getattr(view, 'context', NavigationContext())

        context.push(target=Route.SYSTEM_CHANNELS_MENU)

        view.context = context

        await interaction.response.edit_message(view=view)

    async def _select_new_sys_channel(
            self,
            interaction: discord.Interaction,
            values: list[str]
    ) -> None:
        channel_key = values[0]

        options = self._guilds_text_channels_options(interaction=interaction)

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Select new channel',
            callback=lambda i, v: self._save_new_sys_channel(
                interaction=i,
                channel_key=channel_key,
                values=v
            )
        )

        context = getattr(view, 'context', NavigationContext())

        context.push(target=Route.SYSTEM_CHANNELS_MENU)

        view.context = context

        await interaction.response.edit_message(view=view)

    async def _save_new_sys_channel(
            self,
            interaction: discord.Interaction,
            channel_key: str,
            values: list[str]
    ) -> None:
        channel_id = int(values[0])

        result = await self.service.save_system_channel(
            guild_id=interaction.guild_id,
            channel_data={channel_key: channel_id}
        )

        if not result:
            error_embed = ErrorEmbed(
                description='Something went wrong, please try again later.'
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        await self._send_result_for_update(
            interaction=interaction,
            channel_id=channel_id,
            channel_key=channel_key
        )

    async def _send_result_for_update(
            self,
            interaction: discord.Interaction,
            channel_id: int,
            channel_key: str
    ) -> None:
        channel = interaction.guild.get_channel(channel_id)

        success_embed = SuccessEmbed(
            description=f'For {channel_key} successfully assigned the channel {channel.name}'
        )

        current_channels = await self.formatter.format_current_system_channels(
            guild=interaction.guild
        )

        await interaction.response.edit_message(
            embeds=[success_embed, current_channels]
        )

    # ================================= METHODS FOR DELETE BUTTON =================================
    async def start_for_delete(self, interaction: discord.Interaction) -> None:
        options = self._sys_channels_options(
            guild_id=interaction.guild_id
        )

        if not options:
            embed = ErrorEmbed(
                description='No available channels found.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select a system channel you want to delete:',
            callback=self.delete_sys_channel
        )

        context = getattr(view, 'context', NavigationContext())

        context.push(target=Route.SYSTEM_CHANNELS_MENU)

        view.context = context

        await interaction.response.edit_message(view=view)

    async def delete_sys_channel(self, interaction: discord.Interaction, values: list[str]) -> None:
        result = await self.service.delete_channels(
            guild_id=interaction.guild_id,
            values=values
        )

        if not result:
            embed = ErrorEmbed(
                description='Something went wrong, please try again later.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        await self._send_result_for_delete(
            interaction=interaction,
            values=values
        )

    async def _send_result_for_delete(self, interaction: discord.Interaction, values) -> None:
        is_plural = len(values) != 1

        word_1 = 'Channels' if is_plural else 'Channel'
        word_2 = 'have' if is_plural else 'has'

        msg = f'{word_1} {word_2} been successfully deleted.'

        success_embed = SuccessEmbed(
            description=msg
        )

        current_channels = await self.formatter.format_current_system_channels(guild=interaction.guild)

        await interaction.response.edit_message(embeds=[success_embed, current_channels])

    # ================================= METHODS FOR BOTH BUTTONS =================================
    def _sys_channels_options(self, guild_id: int) -> list[discord.SelectOption]:
        keys = self.service.build_sys_ch_options(guild_id=guild_id)

        return [
            discord.SelectOption(
                label=key.removesuffix('_id').replace('_', ' '),
                value=key
            )
            for key in keys
        ]

    @staticmethod
    def _guilds_text_channels_options(interaction: discord.Interaction) -> list[discord.SelectOption]:
        return [
            discord.SelectOption(
                label=ch.name,
                value=str(ch.id)
            )
            for ch in sorted(
                interaction.guild.text_channels,
                key=lambda ch: ch.name.lower()
            )
        ]

    async def for_sys_channels_list(self, interaction: discord.Interaction) -> None:
        embed = await self.formatter.format_current_system_channels(guild=interaction.guild)
        await interaction.response.edit_message(embed=embed)
