from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget
from features.auto_moderation.verification.flow import VerificationFlow
from features.auto_moderation.verification.service import VerificationService
from features.auto_moderation.verification.views import VerificationView

from ui.embed_constructor.embed_constructor import WarningEmbed

if TYPE_CHECKING:
    from core.bot_config import Bot


class VerificationViewService:
    def __init__(self, bot: Bot, settings: SettingsStorage, service: VerificationService):
        self.bot = bot
        self.settings = settings
        self.service = service
        self.view = None

    async def register_persistent_view(self):
        flow = VerificationFlow(
            bot=self.bot,
            settings=self.settings,
            service=self.service
        )

        self.view = VerificationView(flow=flow)

        self.bot.add_view(view=self.view)

    async def ensure_all_guild_messages(self):
        for guild in self.bot.guilds:
            verification = self.settings.dict_storage.get_value(
                key='verification',
                target=StorageTarget.SETTINGS,
                guild_id=guild.id
            )

            if not verification:
                continue

            channel = await self.service.get_verification_channel(guild=guild)

            if channel is None:
                continue

            await self.ensure_single_message(channel=channel, guild_id=guild.id)

    async def ensure_single_message(self, channel: discord.TextChannel, guild_id: int) -> None:
        found = False
        async for message in channel.history(limit=25):
            if message.author == self.bot.user and message.components:
                found = True
                break

        if not found:
            embed = WarningEmbed(
                description='Please before you agree make sure you have carefully read the rules.'
            )

            message = await channel.send(embed=embed, view=self.view)
            await self.service.save_message_id(
                message_id=message.id,
                guild_id=guild_id
            )
