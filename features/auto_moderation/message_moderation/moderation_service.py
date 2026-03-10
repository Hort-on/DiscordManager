from __future__ import annotations

import time
import xxhash

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings_manager import StorageTarget
from ui.embed_constructor.embed_constructor import WarningEmbed

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage
    from features.auto_moderation.message_moderation.anti_spam_service import AntiSpamService


class ModerationService:
    def __init__(self, settings: SettingsStorage, service: AntiSpamService):
        self.settings = settings
        self.service = service
        self.now = time.monotonic

    async def process_message(self, message: discord.Message) -> None:
        data = self.settings.dict_storage.get_all(
            target=StorageTarget.SETTINGS,
            guild_id=message.guild.id,
        )
        admins = self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=message.guild.id,
        )

        if message.author.id in admins or message.author.id == message.guild.owner_id:
            return

        timestamp = self.now()
        content = message.content
        attachments = message.attachments

        if data.get('flood_checking', False):
            if self.service.check_flood(
                guild_id=message.guild.id,
                user_id=message.author.id,
                timestamp=timestamp,
            ):
                await self._timeout_for_flood(member=message.author)

        if data.get('invitation_blocking', False):
            if 'discord.gg/' in content or 'discord.com/invite/' in content:
                await self._delete_invitation(message=message)

        if data.get('spam_checking', False):
            await self._check_spam(message=message, timestamp=timestamp, attachments=attachments)

    async def _check_spam(
        self,
        message: discord.Message,
        timestamp: float,
        attachments: list[discord.Attachment],
    ) -> None:
        if message.mention_everyone and len(attachments) >= 3:
            await self._timeout_for_spam(messages=[message], guild=message.guild)
            return

        if attachments:
            result = await self.service.check_attachment_spam(message=message, timestamp=timestamp)
            if result.value:
                await self._timeout_for_spam(messages=result.messages, guild=message.guild)
                return

        if 'http' in message.content:
            result = self.service.check_link_spam(message=message, timestamp=timestamp)
            if result.value:
                await self._timeout_for_spam(messages=result.messages, guild=message.guild)
                return

        content_hash = xxhash.xxh64(self.service.normalize_text(message.content)).intdigest()
        result = self.service.check_mass_message(
            content_hash=content_hash,
            message=message,
            timestamp=timestamp,
        )
        if result.value:
            await self._timeout_for_spam(messages=result.messages, guild=message.guild)

    @staticmethod
    async def _timeout_for_flood(member: discord.Member) -> None:
        timeout_until = datetime.now(timezone.utc) + timedelta(minutes=20)
        await member.edit(timed_out_until=timeout_until, reason='Auto moderation: Flood')

    async def _timeout_for_spam(
        self, messages: list[discord.Message], guild: discord.Guild
    ) -> None:
        if not messages:
            return

        timeout_until = datetime.now(timezone.utc) + timedelta(hours=48)
        allowed_ban = self.settings.dict_storage.get_value(
            key='block_users',
            target=StorageTarget.SETTINGS,
            guild_id=guild.id,
        )

        users = {msg.author for msg in messages}
        actioned_names: list[str] = []

        for user in users:
            display_name = user.display_name or user.global_name

            if allowed_ban:
                try:
                    await user.ban(delete_message_days=1, reason='Auto moderation: Raid')
                    actioned_names.append(f'🔸 {display_name} (banned)')
                    continue
                except discord.Forbidden:
                    pass

            await user.edit(timed_out_until=timeout_until, reason='Auto moderation: Raid')
            actioned_names.append(f'🔸 {display_name} (timed out)')

        await self._delete_spam(messages=messages)

        user_list = '\n'.join(actioned_names)
        await self._send_notification(
            guild=guild,
            message=f'The following users were actioned for raiding: \n{user_list}\n and have been banned',
        )

    async def _delete_invitation(self, message: discord.Message) -> None:
        display = message.author.display_name or message.author.global_name

        notification = f'User {display} sent an invite link: {message.content}'
        warning = f'{message.author.mention} only administrators can send invitations on this server.'

        try:
            await message.delete()
        except discord.NotFound:
            return

        await self._send_warning_message(channel=message.channel, message=warning)
        await self._send_notification(guild=message.guild, message=notification)

    async def _send_notification(self, guild: discord.Guild, message: str) -> None:
        channel_id = self.settings.dict_storage.get_value(
            key='notification_channel_id',
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild.id,
        )
        if not channel_id:
            return

        channel = guild.get_channel(channel_id)
        if channel is None:
            return

        await channel.send(embed=WarningEmbed(description=message))

    @staticmethod
    async def _send_warning_message(channel: discord.TextChannel, message: str) -> None:
        try:
            await channel.send(embed=WarningEmbed(description=message))
        except (discord.NotFound, discord.Forbidden):
            pass

    @staticmethod
    async def _delete_spam(messages: list[discord.Message]) -> None:
        from collections import defaultdict

        channels: dict[discord.TextChannel, list[discord.Message]] = defaultdict(list)
        for message in messages:
            channels[message.channel].append(message)

        for channel, msgs in channels.items():
            try:
                if len(msgs) == 1:
                    await msgs[0].delete()
                else:
                    await channel.delete_messages(msgs)
            except discord.HTTPException:
                for msg in msgs:
                    try:
                        await msg.delete()
                    except discord.NotFound:
                        pass
