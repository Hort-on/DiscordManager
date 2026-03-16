from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from ui.embed_constructor.embed_constructor import ErrorEmbed

if TYPE_CHECKING:
    from features.for_admins.delete_message.flow import DeleteMessageFlow
    from general_services.translator.translator import Translator


class DeleteMessagesModal(discord.ui.Modal):
    def __init__(
            self,
            channel: discord.TextChannel,
            flow: DeleteMessageFlow,
            translator: Translator,
            guild_id: int
    ):
        super().__init__(
            title=translator.t(
                guild_id=guild_id,
                section='DELETE_MESSAGES',
                key='delete_msg_title'
            )
        )

        self.channel = channel
        self.flow = flow
        self.translator = translator
        self.guild_id = guild_id

        self.amount = discord.ui.TextInput(
            label=translator.t(
                guild_id=guild_id,
                section='DELETE_MESSAGES',
                key='msg_amount'
            ),
            placeholder=translator.t(
                guild_id=guild_id,
                section='DELETE_MESSAGES',
                key='amount_placeholder'
            ),
            required=True,
            max_length=3
        )

        self.user_names = discord.ui.TextInput(
            label=translator.t(
                guild_id=guild_id,
                section='DELETE_MESSAGES',
                key='ask_user_names'
            ),
            placeholder=translator.t(
                guild_id=guild_id,
                section='DELETE_MESSAGES',
                key='names_placeholder'
            ),
            required=False
        )

        self.add_item(self.amount)
        self.add_item(self.user_names)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        try:
            amount = int(self.amount.value)
        except ValueError:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=interaction.guild_id,
                    section='DELETE_MESSAGES',
                    key='error_number'
                )
            )
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return

        if not 1 <= amount <= 300:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=interaction.guild_id,
                    section='DELETE_MESSAGES',
                    key='wrong_amount'
                )
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
