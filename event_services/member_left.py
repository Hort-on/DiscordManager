from __future__ import annotations

from typing import TYPE_CHECKING

from datetime import datetime, timezone

import discord

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from core.bot_config import Bot
    from general_services.translator.translator import Translator


class MemberLeftNotification:
    def __init__(self, bot: Bot, settings: SettingsStorage, translator: Translator):
        self.bot = bot
        self.settings = settings
        self.translator = translator

    async def check_if_notification(self, member: discord.Member):
        result = self.settings.dict_storage.get_value(
            'member_left',
            target=StorageTarget.SETTINGS,
            guild_id=member.guild.id
        )
        if not result:
            return

        channel_id = self.settings.dict_storage.get_value(
            'notification_channel_id',
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=member.guild.id
        )

        if not channel_id:
            return

        await self.send_notification(member=member, channel_id=channel_id)

    async def send_notification(self, member: discord.Member, channel_id: int):
        channel = self.bot.get_channel(channel_id)

        if not channel:
            return

        guild_id = member.guild.id

        now = datetime.now(timezone.utc)
        duration = now - member.joined_at

        days = duration.days

        embed = discord.Embed(
            title=self.translator.t(
                guild_id=guild_id,
                section='EVENTS',
                key='member_left_title'
            ),
            description=self.translator.t(
                guild_id=guild_id,
                section='EVENTS',
                key='member_left_msg',
                member=member.display_name or member.global_name
            ),
            color=discord.Color.blue(),
            timestamp=now
        )

        embed.add_field(
            name=self.translator.t(
                guild_id=guild_id,
                section='SYSTEM_GENERAL',
                key='user'
            ),
            value=f'{member.mention}',
            inline=False
        )

        embed.add_field(
            name=self.translator.t(
                guild_id=guild_id,
                section='EVENTS',
                key='member_joined',
            ),
            value=f'<t:{int(member.joined_at.timestamp())}:F>',
            inline=False
        )

        embed.add_field(
            name=self.translator.t(
                guild_id=guild_id,
                section='EVENTS',
                key='time_on_server'
            ),
            value=self.translator.t(
                guild_id=guild_id,
                section='EVENTS',
                key='days_on_server',
                days=days
            ),
            inline=False
        )

        await channel.send(embed=embed)
