from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass

from features.auto_moderation.message_moderation.anti_spam_service import AntiSpamService
from features.auto_moderation.message_moderation.moderation_service import ModerationService

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage
    from general_services.translator.translator import Translator


@dataclass
class AutoModModule:
    moderation_service: ModerationService


def build_automod_module(settings: SettingsStorage, translator: Translator) -> AutoModModule:
    anti_spam_service = AntiSpamService(
        settings=settings
    )

    moderation_service = ModerationService(
        settings=settings,
        service=anti_spam_service,
        translator=translator
    )

    return AutoModModule(
        moderation_service=moderation_service
    )
