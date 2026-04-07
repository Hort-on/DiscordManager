from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings_manager import StorageTarget
from general_services.other_services.get_member_by_name import get_member_by_name

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage


class DeleteMessageService:
    def __init__(self, settings: SettingsStorage):
        self.settings = settings

    @staticmethod
    def get_users(guild: discord.Guild, users: str) -> list[discord.Member]:
        user_list: list[discord.Member] = []

        usernames = [name.strip() for name in users.split(",")]

        for username in usernames:
            member = get_member_by_name(guild=guild, username=username)

            if member:
                user_list.append(member)

        return user_list

    def get_channels(self, guild: discord.Guild):
        channels = guild.text_channels

        hidden_channels = self.settings.set_storage.for_set_get(
            target=StorageTarget.HIDDEN_CHANNELS, guild_id=guild.id
        )

        return [channel for channel in channels if channel.id not in hidden_channels]
