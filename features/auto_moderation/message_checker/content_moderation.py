from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage
    from features.auto_moderation.message_checker.content_moderation_service import ContentModerationService


class ContentModerationUI:
    def __init__(self, settings: SettingsStorage, service: ContentModerationService):
        self.settings = settings
        self.service = service

    async def check_message(self, message: discord.Message) -> None:
        data = self.settings.dict_storage.get_all(
            target=StorageTarget.SETTINGS,
            guild_id=message.guild.id
        )

        if data.get('spam_checking', False):
            await self.check_spam(message=message)

        if data.get('bad_words_checking', False):
            await self.check_bad_word(message=message)

        if data.get('invitation_checking', False):
            await self.check_invitation(message=message)

        if data.get('caps_checking', False):
            await self.check_caps(message=message)

    async def check_spam(self, message: discord.Message) -> None:
        spam = self.service.is_spam(message=message)
        if not spam:
            return

    async def check_bad_word(self, message: discord.Message) -> None:
        bad_word = self.service.is_bad_word(message=message)
        if not bad_word:
            return

    async def check_invitation(self, message: discord.Message) -> None:
        invitation = self.service.is_invitation(message=message)
        if not invitation:
            return

    async def check_caps(self, message: discord.Message) -> None:
        caps = self.service.is_caps(message=message)
        if not caps:
            return
