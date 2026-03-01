from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import discord

from database.db_base_service import DBBaseService
from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.settings_storage.settings import SettingsStorage
    from database.db_factory.db_scenario_factory import DBFactory


@dataclass
class AssignVerificationRoleResult:
    value: bool
    message: str


class VerificationService(DBBaseService):
    def __init__(self, bot: Bot, settings: SettingsStorage, db_factory: DBFactory):
        super().__init__(settings)

        self.bot = bot
        self.settings = settings
        self.db_factory = db_factory

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

    async def assign_role(self, guild: discord.Guild, member: discord.Member) -> AssignVerificationRoleResult:
        verification_role = self.settings.dict_storage.get_value(
            'verification_role_id',
            target=StorageTarget.SETTINGS,
            guild_id=guild.id
        )

        if not verification_role:
            message = 'Verification role is not assigned yet, please contact with the admins of the server.'

            return AssignVerificationRoleResult(
                value=False,
                message=message
            )

        role = guild.get_role(verification_role)
        if not role:
            message = 'Verification role was not found.'
            return AssignVerificationRoleResult(
                value=False,
                message=message
            )

        await member.add_roles(role)

        self.users_count.pop((member.id, guild.id), None)

        message = 'Congratulations! Welcome to our community. For additional info, please use "/help"'
        return AssignVerificationRoleResult(
            value=True,
            message=message
        )

    async def save_message_id(self, message_id: int, guild_id: int) -> None:
        save_message = self.db_factory.for_write_data(
            guild_id=guild_id,
            table_name='settings',
            data={'verification_message_id': message_id}
        )

        await self.update_db_and_cache(
            scenario=save_message,
            guild_id=guild_id
        )

    async def get_verification_channel(self, guild: discord.Guild) -> discord.TextChannel | None:
        channel_id = self.settings.dict_storage.get_value(
            'verification_channel_id',
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild.id
        )

        if not channel_id:
            return None

        channel = guild.get_channel(channel_id)

        if not channel:
            try:
                channel = await self.bot.fetch_channel(channel_id)
            except discord.NotFound:
                return None

        if isinstance(channel, discord.TextChannel):
            return channel

        return None
