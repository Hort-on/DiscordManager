from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.routes import Route

from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.embed_constructor.embed_constructor import SuccessEmbed, ErrorEmbed

from features.for_admins.edit_settings.services.system_channels import SystemChannelsService
from features.for_admins.edit_settings.services.settings_formatter import SettingsFormatter

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from general_services.translator.translator import Translator


class SystemChannelsFlow:
    def __init__(
            self,
            navigator: Navigator,
            context: NavigationContext,
            sys_channels_service: SystemChannelsService,
            formatter: SettingsFormatter,
            translator: Translator
    ):

        self.navigator = navigator
        self.context = context
        self.service = sys_channels_service
        self.formatter = formatter
        self.translator = translator

    # ================================= METHODS FOR ADD BUTTON =================================
    async def start_for_add(self, interaction: discord.Interaction) -> None:
        options = self._sys_channels_options(
            guild_id=interaction.guild_id
        )

        if not options:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=interaction.guild_id,
                    section='EDIT_SETTINGS',
                    key='no_available_ch'
                )
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder=self.translator.t(
                guild_id=interaction.guild_id,
                section='EDIT_SETTINGS',
                key='ask_sys_ch'
            ),
            callback=self._select_new_sys_channel
        )

        view.context = self.context

        self.context.push(target=Route.SYSTEM_CHANNELS_MENU)

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
            placeholder=self.translator.t(
                guild_id=interaction.guild_id,
                section='EDIT_SETTINGS',
                key='ask_new_sys_ch'
            ),
            callback=lambda i, v: self._save_new_sys_channel(
                interaction=i,
                channel_key=channel_key,
                values=v
            )
        )

        view.context = self.context

        self.context.push(target=Route.SETTINGS_MENU)

        await interaction.response.edit_message(view=view)

    async def _save_new_sys_channel(
            self,
            interaction: discord.Interaction,
            channel_key: str,
            values: list[str]
    ) -> None:
        channel_id = int(values[0])

        result = await self.service.save_system_channel(
            guild=interaction.guild,
            channel_data={channel_key: channel_id}
        )

        if not result:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=interaction.guild_id,
                    section='SYSTEM_GENERAL',
                    key='error_msg'
                )
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
            description=self.translator.t(
                guild_id=interaction.guild_id,
                section='EDIT_SETTINGS',
                key='sys_ch_success',
                channel_key=channel_key,
                channel_name=channel.name
            ),
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
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=interaction.guild_id,
                    section='EDIT_SETTINGS',
                    key='no_available_ch'
                )
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder=self.translator.t(
                guild_id=interaction.guild_id,
                section='EDIT_SETTINGS',
                key='ask_sys_ch_to_delete'
            ),
            callback=self.delete_sys_channel
        )

        view.context = self.context

        self.context.push(target=Route.SETTINGS_MENU)

        await interaction.response.edit_message(view=view)

    async def delete_sys_channel(self, interaction: discord.Interaction, values: list[str]) -> None:
        result = await self.service.delete_channels(
            guild_id=interaction.guild_id,
            values=values
        )

        if not result:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=interaction.guild_id,
                    section='SYSTEM_GENERAL',
                    key='error_msg'
                )
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        await self._send_result_for_delete(interaction=interaction)

    async def _send_result_for_delete(self, interaction: discord.Interaction) -> None:
        success_embed = SuccessEmbed(
            description=self.translator.t(
                guild_id=interaction.guild_id,
                section='EDIT_SETTINGS',
                key='success_sys_ch_deletion'
            )
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
