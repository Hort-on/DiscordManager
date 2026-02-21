from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator_context import NavigationContext
from features.for_admins.delete_message.modals import DeleteMessagesModal

from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed

if TYPE_CHECKING:
    from features.for_admins.delete_message.service import DeleteMessageService
    from core.navigator import Navigator


class DeleteMessageFlow:
    def __init__(
            self,
            delete_msg_service: DeleteMessageService,
            navigator: Navigator
    ):
        self.service = delete_msg_service
        self.navigator = navigator

    async def delete_message_start(self, interaction: discord.Interaction) -> None:
        options = self._build_options(guild=interaction.guild)

        if not options:
            embed = ErrorEmbed(
                description=f'The guild does not have text channels.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the channel:',
            callback=self._send_modal
        )

        context = getattr(view, 'context', NavigationContext())

        context.push(target='admin_menu', params={'guild_id': interaction.guild_id})

        view.context = context

        await interaction.response.edit_message(view=view)

    async def delete_message(
            self,
            interaction: discord.Interaction,
            channel: discord.TextChannel,
            amount: int,
            users: str | None
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        users_names = users.strip() if users else None

        if not users_names:
            len_result = await self.service.delete_any_message_process(
                channel=channel,
                amount=amount
            )

            if len_result == 0:
                error_embed = ErrorEmbed(
                    description='No messages were found in the selected channel or from the selected users.'
                )
                await interaction.followup.send(
                    embed=error_embed
                )
            else:
                success_embed = SuccessEmbed(
                    description=f'{len_result} messages were successfully deleted from the channel: {channel.name}.'
                )
                await interaction.followup.send(
                    embed=success_embed
                )
                return

        result = await self.service.delete_message_from_users(
            guild=interaction.guild,
            channel=channel,
            amount=amount,
            users=users_names
        )
        if not result:
            error_embed = ErrorEmbed(
                description='No messages were found in the selected channel or from the selected users.'
            )
            await interaction.followup.send(
                embed=error_embed
            )
            return

        success_embed = SuccessEmbed(
            description=result
        )
        await interaction.followup.send(
            embed=success_embed
        )

    async def _send_modal(self, interaction: discord.Interaction, value: list[str]) -> None:
        channel_id = int(value[0])
        channel = interaction.client.get_channel(channel_id)

        await interaction.response.send_modal(DeleteMessagesModal(
            channel=channel,
            service=self.service,
            navigator=self.navigator,
            flow=self
        ))

    def _build_options(self, guild: discord.Guild) -> list[discord.SelectOption]:
        channels = self.service.get_channels(guild=guild)

        return [
            discord.SelectOption(
                label=channel.name,
                value=str(channel.id)
            )
            for channel in channels
        ]
