from __future__ import annotations

import time

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings_manager import StorageTarget

from ui.embed_constructor.embed_constructor import WarningEmbed

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage
    from features.auto_moderation.message_moderation.anti_spam_service import AntiSpamService
    from general_services.translator.translator import Translator


class ModerationService:
    def __init__(self, settings: SettingsStorage, service: AntiSpamService, translator: Translator):
        self.settings = settings
        self.service = service
        self.now = time.monotonic
        self.translator = translator

    async def process_message(self, message: discord.Message) -> None:
        if message.guild is None:
            return

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
                if isinstance(message.author, discord.Member):
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
        if not message.guild:
            return

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

    async def _timeout_for_flood(self, member: discord.Member) -> None:
        timeout_until = datetime.now(timezone.utc) + timedelta(minutes=20)
        await member.edit(
            timed_out_until=timeout_until,
            reason=self.translator.t(
                guild_id=member.guild.id,
                section='MODERATION',
                key='flood'
            )
        )

    async def _timeout_for_spam(self, messages: list[discord.Message], guild: discord.Guild) -> None:
        if not messages:
            return

        guild_id = guild.id

        timeout_until = datetime.now(timezone.utc) + timedelta(hours=48)
        allowed_ban = self.settings.dict_storage.get_value(
            key='block_users',
            target=StorageTarget.SETTINGS,
            guild_id=guild.id,
        )

        users = {msg.author for msg in messages}
        actioned_names: list[str] = []
        not_banned: list[str] = []

        for user in users:
            if not isinstance(user, discord.Member):
                continue

            name = user.display_name or user.global_name

            if user.top_role >= guild.me.top_role:
                not_banned.append(f'🔸 {name}')
                continue

            if allowed_ban:
                try:
                    await user.ban(
                        delete_message_days=1,
                        reason=self.translator.t(
                            guild_id=guild_id,
                            section='MODERATION',
                            key='raid'
                        )
                    )
                    actioned_names.append(
                        self.translator.t(
                            guild_id=guild_id,
                            section='MODERATION',
                            key='banned',
                            display_name=name
                        )
                    )
                    continue
                except (discord.Forbidden, discord.HTTPException) as e:
                    print(f"Ban failed: {e}")

            await user.edit(
                timed_out_until=timeout_until,
                reason=self.translator.t(
                    guild_id=guild_id,
                    section='MODERATION',
                    key='raid'
                )
            )

            self.service.clear_user(guild_id=guild.id, user_id=user.id)

            actioned_names.append(
                self.translator.t(
                    guild_id=guild_id,
                    section='MODERATION',
                    key='timed_out',
                    display_name=name
                )
            )

        await self._delete_spam(messages=messages)

        user_list = '\n'.join(actioned_names)

        messages_to_sent: list[str] = [self.translator.t(
            guild_id=guild_id,
            section='MODERATION',
            key='actioned_users',
            user_list=user_list
        )]

        if not_banned:
            messages_to_sent.append(
                self.translator.t(
                    guild_id=guild_id,
                    section='MODERATION',
                    key='actioned_users_not_banned',
                    not_banned='\n'.join(not_banned)
                )
            )

        await self._send_notification(
            guild=guild,
            message='\n'. join(messages_to_sent),
        )

    async def _delete_invitation(self, message: discord.Message) -> None:
        if not message.guild:
            return

        name = message.author.display_name or message.author.global_name

        notification = self.translator.t(
            guild_id=message.guild.id,
            section='MODERATION',
            key='invite_notification',
            name=name
        )

        warning = self.translator.t(
            guild_id=message.guild.id,
            section='MODERATION',
            key='invite_warning',
            mention=message.author.mention
        )

        try:
            await message.delete()
        except discord.NotFound:
            return

        if isinstance(message.channel, discord.TextChannel):
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
        if not isinstance(channel, discord.TextChannel):
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
            if isinstance(message.channel, discord.TextChannel):
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
