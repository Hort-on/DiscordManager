from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage
    from core.bot_config import Bot
    from core.container import BotContainer

import discord

from core.container import AppContainer

from database.settings_storage.settings_manager import StorageTarget

from modules.verification.view import VerificationView

from ui.embed_constructor.embed_constructor import WarningEmbed


class CheckVerification:
    def __init__(self, settings: SettingsStorage, bot: Bot):
        self.bot = bot
        self.settings = settings

    async def prepare(self):
        self.bot.add_view(VerificationView(
            settings=self.settings,
            yes_no_factory=self.container.yes_no_factory
        ))

        for guild in self.bot.guilds:
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

            if data.get('verification', None) and channel_id is not None:
                channel = guild.get_channel(channel_id)
                if not channel:
                    try:
                        channel = await self.bot.fetch_channel(channel_id)
                    except discord.NotFound:
                        continue

                if isinstance(channel, discord.TextChannel):
                    view = VerificationView(
                        settings=self.settings,
                        yes_no_factory=self.container.yes_no_factory
                    )

                    await self.ensure_verification_message(channel, view)

    async def ensure_verification_message(self, channel, view):
        found = False
        async for message in channel.history(limit=25):
            if message.author == self.bot.user and message.components:
                found = True
                break

        if not found:
            embed = WarningEmbed(
                description='Please before you agree make sure you have carefully read the rules.'
            )

            await channel.send(embed=embed, view=view)
