from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from ui.embed_constructor.embed_constructor import ErrorEmbed, InfoEmbed

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_admins.send_messages.services.send_rules_service import RulesService
    from general_services.translator.translator import Translator


class SendRulesFlow:
    def __init__(
            self,
            navigator: Navigator,
            rules_service: RulesService,
            translator: Translator
    ):
        self.navigator = navigator
        self.service = rules_service
        self.translator = translator

    async def start_for_rules(self, interaction: discord.Interaction):
        guild = interaction.guild
        assert guild is not None

        channel_id = self.service.get_verification_channel(guild_id=guild.id)
        if not channel_id:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=guild.id,
                    section='SEND_MSG',
                    key='assure_ch'
                )
            )
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return

        self.service.active_sessions[interaction.user.id] = guild.id

        embed = InfoEmbed(
            description=self.translator.t(
                guild_id=guild.id,
                section='SEND_MSG',
                key='ask_msg_dm'
            )
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)
