from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass

from features.auto_moderation.message_moderation.anti_spam_service import AntiSpamService
from features.auto_moderation.message_moderation.moderation_service import ModerationService

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage


@dataclass
class AutoModModule:
    moderation_service: ModerationService


def build_automod_module(settings: SettingsStorage) -> AutoModModule:
    anti_spam_service = AntiSpamService(
        settings=settings
    )

    moderation_service = ModerationService(
        settings=settings,
        service=anti_spam_service
    )

    return AutoModModule(
        moderation_service=moderation_service
    )
