from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed

if TYPE_CHECKING:
    from features.for_everyone.temp_voice_channel.service import (
        TempVoiceChannelService,
    )
    from general_services.translator.translator import Translator


class CreateTempVoiceChannelButton(discord.ui.Button):
    def __init__(
        self,
        service: TempVoiceChannelService,
        translator: Translator,
        guild_id: int,
    ):
        super().__init__(
            label=translator.t(
                guild_id=guild_id, section="TEMP_CHANNELS", key="create_button"
            ),
            style=discord.ButtonStyle.secondary,
        )

        self.service = service
        self.translator = translator

    async def callback(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        user = interaction.user

        if guild is None or not isinstance(user, discord.Member):
            return

        result = await self.service.create_channel(guild=guild, member=user)
        channel_name = result.channel.name if result.channel else ""
        message = self.translator.t(
            guild_id=guild.id,
            section="TEMP_CHANNELS",
            key=result.message_key,
            channel_name=channel_name,
        )

        embed_class = SuccessEmbed if result.success else ErrorEmbed
        await interaction.response.send_message(
            embed=embed_class(description=message),
            ephemeral=True,
        )
