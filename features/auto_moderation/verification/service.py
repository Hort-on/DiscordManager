from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.settings_storage.settings import SettingsStorage


class VerificationService:
    def __init__(self, bot: Bot, settings: SettingsStorage):
        self.bot = bot
        self.settings = settings
        self.users_count: dict[tuple[int, int], int] = {}

    async def check_the_word(
            self,
            guild_id: int,
            member: discord.Member,
            word: str
    ) -> bool:
        if word.lower() != 'hello':
            key = (member.id, guild_id)

            count = self.users_count.get(key, 0) + 1
            self.users_count[key] = count

            if count >= 2:
                try:
                    await member.kick(reason='has not passed verification')
                except discord.Forbidden:
                    pass
                finally:
                    self.users_count.pop(key, None)

            return False

        return True

    async def assign_role(self, guild: discord.Guild, member: discord.Member) -> tuple:
        data = self.settings.dict_storage.for_dict_get(
            'verification_role_id',
            target=StorageTarget.SETTINGS,
            guild_id=guild.id
        )

        verification_role = data.get('verification_role_id')

        if not verification_role:
            message = 'Verification role is not assigned yet, please contact with the admins of the server.'

            return False, message

        role = guild.get_role(verification_role)
        if not role:
            return False, "Verification role was not found."

        await member.add_roles(role)

        self.users_count.pop((member.id, guild.id), None)

        message = 'Congratulations! Welcome to our community. For additional info, please use "/help"'
        return True, message

    async def is_verification_enabled(self, guild: discord.Guild) -> discord.TextChannel | None:
        data = self.settings.dict_storage.for_dict_get(
            'verification',
            target=StorageTarget.SETTINGS,
            guild_id=guild.id
        )

        verification_channel = self.settings.dict_storage.for_dict_get(
            'verification_channel_id',
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild.id
        )

        channel_id = verification_channel.get('verification_channel_id')

        channel = guild.get_channel(channel_id)

        if not channel:
            try:
                channel = await self.bot.fetch_channel(channel_id)
            except discord.NotFound:
                return None

        if data.get('verification', None) and channel is not None:
            return channel

        return None
