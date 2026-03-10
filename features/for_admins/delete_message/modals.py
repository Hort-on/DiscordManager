from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from ui.embed_constructor.embed_constructor import ErrorEmbed

if TYPE_CHECKING:
    from features.for_admins.delete_message.flow import DeleteMessageFlow


class DeleteMessagesModal(discord.ui.Modal, title='Delete messages'):
    def __init__(
            self,
            channel: discord.TextChannel,
            flow: DeleteMessageFlow
    ):
        super().__init__()
        self.channel = channel
        self.flow = flow

    amount = discord.ui.TextInput(
        label='How many messages do you want to delete?',
        placeholder='Please enter a number between 1 and 100',
        required=True,
        max_length=3
    )

    user_names = discord.ui.TextInput(
        label='Type user names',
        placeholder='Please type general user names like: user123, user_2, user etc. separated by coma.',
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        try:
            amount = int(self.amount.value)
        except ValueError:
            error_embed = ErrorEmbed(
                description='Amount must be a number.'
            )
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return

        if not 1 <= amount <= 300:
            error_embed = ErrorEmbed(
                description='Amount must be between 1 and 300.'
            )
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return

        await self.flow.delete_message(
            interaction=interaction,
            channel=self.channel,
            amount=amount,
            users=self.user_names.value
        )
