from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_admins.send_messages.services.send_message_service import MessageService
    from general_services.translator.translator import Translator


class SendMessageFlow:
    def __init__(
            self,
            message_service: MessageService,
            navigator: Navigator,
            translator: Translator
    ):
        self.service = message_service
        self.navigator = navigator
        self.translator = translator

    async def start_for_send(self, interaction: discord.Interaction):
        guild = interaction.guild
        assert guild is not None

        options = self.service.get_channels(guild=guild)

        if not options:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=guild.id,
                    section='SYSTEM_GENERAL',
                    key='no_available_ch'
                )
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            translator=self.translator,
            guild_id=guild.id,
            placeholder=self.translator.t(
                guild_id=guild.id,
                section='SEND_MSG',
                key='ask_ch_to_send'
            ),
            callback=self._handle_channel,
        )

        await interaction.response.edit_message(
            view=view
        )

    async def _handle_channel(self, interaction: discord.Interaction, value: list[str]):
        guild = interaction.guild
        assert guild is not None

        channel = guild.get_channel(int(value[0]))
        if not channel:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=guild.id,
                    section='SYSTEM_GENERAL',
                    key='error_msg'
                )
            )
            await interaction.response.edit_message(
                embed=error_embed
            )
            return

        result = await self.service.save_channel(
            guild_id=guild.id,
            user_id=interaction.user.id,
            channel_id=channel.id
        )

        if not result:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=guild.id,
                    section='SYSTEM_GENERAL',
                    key='error_msg'
                )
            )
            await interaction.response.edit_message(
                embed=error_embed
            )
            return

        success_embed = SuccessEmbed(
            description=self.translator.t(
                guild_id=guild.id,
                section='SEND_MSG',
                key='success_ch_to_send',
                channel_name=channel.name
            )
        )

        await interaction.response.edit_message(
            embed=success_embed
        )
