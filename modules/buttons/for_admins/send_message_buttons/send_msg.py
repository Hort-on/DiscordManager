from __future__ import annotations

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from services.embed_constructor.embed_constructor import WarningEmbed

from services.other_services.get_channel import ChannelSelectorManager
from services.factories.channel_factory.scenarios_factory import ChannelFactory

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator


class SendMessageButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Send message',
            style=discord.ButtonStyle.blurple
        )

    async def on_click(self, interaction: discord.Interaction):
        scenario = ChannelFactory.for_db_message_save()

        manager = ChannelSelectorManager(scenario=scenario, text_only=True)

        try:
            await interaction.user.create_dm()
            await manager.select_channel_type(interaction=interaction)
        except discord.Forbidden:
            embed = WarningEmbed(
                description='Please open your Direct Message'
            )
            await interaction.response.edit_message(embed=embed)
