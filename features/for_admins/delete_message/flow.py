from __future__ import annotations

from typing import TYPE_CHECKING, Counter

import discord

from core.navigator.params_containers import AdminMenuParams
from core.navigator.routes import Route

from features.for_admins.delete_message.modals import DeleteMessagesModal

from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from features.for_admins.delete_message.service import DeleteMessageService
    from general_services.translator.translator import Translator


class DeleteMessageFlow:
    def __init__(
            self,
            delete_msg_service: DeleteMessageService,
            navigator: Navigator,
            context: NavigationContext,
            translator: Translator
    ):

        self.navigator = navigator
        self.context = context
        self.service = delete_msg_service
        self.translator = translator

    async def delete_message_start(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        assert guild is not None

        options = self._build_options(guild=guild)

        if not options:
            embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=guild.id,
                    section='SYSTEM_GENERAL',
                    key='not_found_channels'
                )
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            translator=self.translator,
            guild_id=guild.id,
            placeholder=self.translator.t(
                guild_id=guild.id,
                section='SYSTEM_GENERAL',
                key='ask_for_channel'
            ),
            callback=self._send_modal
        )

        view.context = self.context
        self.context.push(
            target=Route.ADMIN_MENU,
            params=AdminMenuParams(guild_id=guild.id)
        )

        await interaction.response.edit_message(view=view)

    async def delete_message(
            self,
            interaction: discord.Interaction,
            channel: discord.TextChannel,
            amount: int,
            users: str | None
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild
        assert guild is not None

        users_names = users.strip() if users else None

        if users_names:
            result = await self._delete_message_from_users(
                guild=guild,
                channel=channel,
                amount=amount,
                users_list=users_names
            )

            if not result:
                embed = ErrorEmbed(
                    description=self.translator.t(
                        guild_id=guild.id,
                        section='SYSTEM_GENERAL',
                        key='msg_not_found'
                    )
                )
            else:
                embed = SuccessEmbed(description=result)

            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        len_result = await self._delete_any_message_process(
            channel=channel,
            amount=amount
        )

        if len_result == 0:
            embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=guild.id,
                    section='SYSTEM_GENERAL',
                    key='msg_not_found'
                )
            )
        else:
            embed = SuccessEmbed(
                description=self.translator.t(
                    guild_id=guild.id,
                    section='DELETE_MESSAGES',
                    key='success_msg_deletion',
                    len_result=len_result,
                    channel_name=channel.name
                )
            )

        await interaction.followup.send(embed=embed, ephemeral=True)

    async def _send_modal(self, interaction: discord.Interaction, value: list[str]) -> None:
        guild = interaction.guild
        assert guild is not None

        channel_id = int(value[0])
        channel = interaction.client.get_channel(channel_id)

        if not isinstance(channel, discord.TextChannel):
            return

        await interaction.response.send_modal(
            DeleteMessagesModal(
                channel=channel,
                flow=self,
                translator=self.translator,
                guild_id=guild.id
            )
        )

    def _build_options(self, guild: discord.Guild) -> list[discord.SelectOption]:
        channels = self.service.get_channels(guild=guild)

        return [
            discord.SelectOption(
                label=channel.name,
                value=str(channel.id)
            )
            for channel in channels
        ]

    async def _delete_message_from_users(
            self,
            guild: discord.Guild,
            channel: discord.TextChannel,
            amount: int,
            users_list: str
    ) -> str | None:
        user_names = self.service.get_users(
            guild=guild,
            users=users_list
        )

        result_msg = []

        users = set(user_names)

        def _check(m) -> bool:
            return m.author in users

        deleted = await channel.purge(
            limit=amount,
            check=_check
        )

        if not deleted:
            return None

        counter = Counter(msg.author.display_name for msg in deleted)
        for user_name, count in counter.items():
            result_msg.append(
                self.translator.t(
                    guild_id=guild.id,
                    section='DELETE_MESSAGES',
                    key='success_msg_del_user',
                    count=count,
                    user_name=user_name
                )
            )

        final_msg = ''.join(result_msg)

        return final_msg

    @staticmethod
    async def _delete_any_message_process(
            channel: discord.TextChannel,
            amount: int
    ) -> int:
        deleted = await channel.purge(limit=amount)
        return 0 if not deleted else len(deleted)
