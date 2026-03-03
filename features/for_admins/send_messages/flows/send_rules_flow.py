from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from ui.embed_constructor.embed_constructor import ErrorEmbed

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_admins.send_messages.services.send_rules_service import RulesService


class SendRulesFlow:
    def __init__(self, navigator: Navigator, rules_service: RulesService):
        self.navigator = navigator
        self.service = rules_service

    async def start_for_rules(self, interaction: discord.Interaction):
        channel = self.service.get_verification_channel(
            guild_id=interaction.guild_id
        )
        if not channel:
            embed = ErrorEmbed(
                description='Please before sending rules, please assign verification channel.'
            )
            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )
            return

        self.service.active_sessions[interaction.user.id] = interaction.guild_id

        await interaction.response.send_message(
            'Please send your rules to the bot`s DM.',
            ephemeral=True
        )
