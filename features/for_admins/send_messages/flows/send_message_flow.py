from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_admins.send_messages.services.send_message_service import MessageService


class SendMessageFlow:
    def __init__(
            self,
            message_service: MessageService,
            navigator: Navigator
    ):
        self.service = message_service
        self.navigator = navigator

    async def start_for_send(self, interaction: discord.Interaction):
        options = self.service.get_channels(
            guild=interaction.guild
        )

        if not options:
            embed = ErrorEmbed(
                description='No available roles to be add.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the channel you want to send messages:',
            callback=self._handle_channel,
        )

        await interaction.response.edit_message(
            view=view
        )

    async def _handle_channel(self, interaction: discord.Interaction, value: list[str]):
        channel = interaction.guild.get_channel(int(value[0]))

        print(channel.name, channel.id)
        result = await self.service.save_channel(
            guild_id=interaction.guild_id,
            user_id=interaction.user.id,
            channel_id=channel.id
        )

        if not result:
            error_embed = ErrorEmbed(
                description='Something went wrong, please try again later.'
            )
            await interaction.response.edit_message(
                embed=error_embed
            )
            return

        success_embed = SuccessEmbed(
            description=f'Successful, now all you can send anon messages. Selected channel: {channel.name}. \n'
                        f'To send messages just send it to the bot in DM.'
        )

        await interaction.response.edit_message(
            embed=success_embed
        )
