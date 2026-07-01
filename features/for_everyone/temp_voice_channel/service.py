from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory


@dataclass
class TempChannelResult:
    success: bool
    message_key: str
    channel: discord.VoiceChannel | None = None


class TempVoiceChannelService:
    def __init__(self, db_factory: DBFactory):
        self.db_factory = db_factory

    async def create_channel(
        self, guild: discord.Guild, member: discord.Member
    ) -> TempChannelResult:
        existing = await self._get_existing_channel(guild=guild, owner_id=member.id)

        if existing:
            return TempChannelResult(
                success=False,
                message_key="already_exists",
                channel=existing,
            )

        category = None
        if member.voice and isinstance(member.voice.channel, discord.VoiceChannel):
            category = member.voice.channel.category

        name = self._build_channel_name(member=member)
        overwrites = self._build_overwrites(guild=guild, member=member)

        try:
            channel = await guild.create_voice_channel(
                name=name,
                category=category,
                overwrites=overwrites,
                reason=f"Temporary channel created by {member}",
            )
        except discord.Forbidden:
            return TempChannelResult(success=False, message_key="missing_permissions")
        except discord.HTTPException:
            return TempChannelResult(success=False, message_key="creation_failed")

        scenario = self.db_factory.for_save_temp_channel(
            guild_id=guild.id, channel_id=channel.id, owner_id=member.id
        )
        await scenario.db_proceed()

        if member.voice:
            try:
                await member.move_to(channel)
            except discord.HTTPException:
                pass

        return TempChannelResult(success=True, message_key="created", channel=channel)

    async def delete_if_empty(self, channel: discord.VoiceChannel) -> None:
        if channel.guild is None or channel.members:
            return

        scenario = self.db_factory.for_get_temp_channel(
            guild_id=channel.guild.id, channel_id=channel.id
        )
        row = await scenario.db_proceed()

        if not row:
            return

        await self.delete_record(guild_id=channel.guild.id, channel_id=channel.id)

        try:
            await channel.delete(reason="Temporary channel is empty")
        except (discord.Forbidden, discord.NotFound, discord.HTTPException):
            pass

    async def delete_record(self, guild_id: int, channel_id: int) -> None:
        scenario = self.db_factory.for_delete_temp_channel(
            guild_id=guild_id, channel_id=channel_id
        )
        await scenario.db_proceed()

    async def _get_existing_channel(
        self, guild: discord.Guild, owner_id: int
    ) -> discord.VoiceChannel | None:
        scenario = self.db_factory.for_get_temp_channel_by_owner(
            guild_id=guild.id, owner_id=owner_id
        )
        row = await scenario.db_proceed()

        if not row:
            return None

        channel = guild.get_channel(row["channel_id"])

        if isinstance(channel, discord.VoiceChannel):
            return channel

        await self.delete_record(guild_id=guild.id, channel_id=row["channel_id"])
        return None

    @staticmethod
    def _build_channel_name(member: discord.Member) -> str:
        display_name = member.display_name or member.name
        return f"{display_name}'s channel"[:100]

    @staticmethod
    def _build_overwrites(
        guild: discord.Guild, member: discord.Member
    ) -> dict[discord.Role | discord.Member, discord.PermissionOverwrite]:
        return {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=True,
                connect=True,
                speak=True,
            ),
            member: discord.PermissionOverwrite(
                view_channel=True,
                connect=True,
                speak=True,
                stream=True,
                manage_channels=True,
                manage_roles=True,
                mute_members=True,
                deafen_members=True,
                move_members=True,
            ),
        }
