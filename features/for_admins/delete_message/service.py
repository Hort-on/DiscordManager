from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from collections import Counter

from database.settings_storage.settings_manager import StorageTarget
from general_services.other_services.get_member_by_name import get_member_by_name

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage


class DeleteMessageService:
    def __init__(self, settings: SettingsStorage):
        self.settings = settings

    @staticmethod
    async def delete_any_message_process(
            channel: discord.TextChannel,
            amount: int
    ) -> int:
        deleted = await channel.purge(limit=amount)
        return 0 if not deleted else len(deleted)

    async def delete_message_from_users(
            self,
            guild: discord.Guild,
            channel: discord.TextChannel,
            amount: int,
            users: str
    ) -> str | bool:
        user_names = self._get_users(
            guild=guild,
            users=users
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
            return False

        counter = Counter(msg.author.display_name for msg in deleted)
        for user_name, count in counter.items():
            result_msg.append(
                f'Successfully deleted {count} messages from user: {user_name}\n'
            )

        final_msg = ''.join(result_msg)

        return final_msg

    @staticmethod
    def _get_users(guild: discord.Guild, users: str) -> list[discord.Member]:
        user_list: list[discord.Member] = []

        usernames = [name.strip() for name in users.split(',')]

        for username in usernames:
            member = get_member_by_name(
                guild=guild,
                username=username
            )

            if member:
                user_list.append(member)

        return user_list

    def get_channels(self, guild: discord.Guild):
        channels = guild.text_channels

        hidden_channels = self.settings.set_storage.for_set_get(
            target=StorageTarget.HIDDEN_CHANNELS,
            guild_id=guild.id
        )

        return [channel for channel in channels if channel.id not in hidden_channels]
