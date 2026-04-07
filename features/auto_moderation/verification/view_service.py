from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget
from features.auto_moderation.verification.flow import VerificationFlow
from features.auto_moderation.verification.service import VerificationService
from features.auto_moderation.verification.view import VerificationView
from ui.embed_constructor.embed_constructor import WarningEmbed

if TYPE_CHECKING:
    from core.bot_config import Bot
    from general_services.translator.translator import Translator


class VerificationViewService:
    def __init__(
        self,
        bot: Bot,
        settings: SettingsStorage,
        service: VerificationService,
        translator: Translator,
    ):
        self.bot = bot
        self.settings = settings
        self.service = service
        self.translator = translator
        self.view = None

    async def register_persistent_view(self):
        flow = VerificationFlow(
            bot=self.bot,
            settings=self.settings,
            service=self.service,
            translator=self.translator,
        )

        self.view = VerificationView(flow=flow)

        self.bot.add_view(view=self.view)

    async def ensure_all_guild_messages(self):
        for guild in self.bot.guilds:
            verification = self.settings.dict_storage.get_value(
                key="verification", target=StorageTarget.SETTINGS, guild_id=guild.id
            )

            if not verification:
                continue

            channel = await self.service.get_verification_channel(guild=guild)

            if channel is None:
                continue

            await self.ensure_single_message(channel=channel, guild_id=guild.id)

    async def ensure_single_message(
        self, channel: discord.TextChannel, guild_id: int
    ) -> None:
        found = False
        async for message in channel.history(limit=25):
            if message.author == self.bot.user and message.components:
                found = True
                await self.service.save_message_id(
                    message_id=message.id, guild_id=guild_id
                )
                break

        if not found:
            embed = WarningEmbed(
                description=self.translator.t(
                    guild_id=guild_id, section="VERIFICATION", key="ensure_msg"
                )
            )

            flow = VerificationFlow(
                bot=self.bot,
                settings=self.settings,
                service=self.service,
                translator=self.translator,
            )

            view = VerificationView(flow=flow)

            for item in view.children:
                item: discord.ui.Button

                if item.custom_id == "verify_agree":
                    item.label = self.translator.t(
                        guild_id=guild_id, section="VERIFICATION", key="agree_button"
                    )
                elif item.custom_id == "verify_disagree":
                    item.label = self.translator.t(
                        guild_id=guild_id, section="VERIFICATION", key="disagree_button"
                    )

            message = await channel.send(embed=embed, view=view)
            await self.service.save_message_id(message_id=message.id, guild_id=guild_id)
