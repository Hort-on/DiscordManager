from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.for_everyone.birthdays.buttons import (
    AddBirthdayButton,
    AddForAdmins,
    DeleteBirthdayButton,
    DeleteForAdmins,
)
from ui.buttons.back_button import BackButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_everyone.birthdays.flow import BirthdayFlow
    from general_services.translator.translator import Translator
    from ui.button_protection.button_protection_service import ButtonProtectionService


class BirthdayMenuView(discord.ui.View):
    def __init__(
        self,
        navigator: Navigator,
        flow: BirthdayFlow,
        translator: Translator,
        protection_service: ButtonProtectionService,
        admins: set[int],
        guild_id: int,
        user_id: int,
        owner_id: int | None,
    ):
        super().__init__(timeout=60)

        self.add_item(
            AddBirthdayButton(flow=flow, translator=translator, guild_id=guild_id)
        )
        self.add_item(
            DeleteBirthdayButton(flow=flow, translator=translator, guild_id=guild_id)
        )
        self.add_item(
            BackButton(navigator=navigator, translator=translator, guild_id=guild_id)
        )

        if user_id in admins or user_id == owner_id:
            self.add_item(
                AddForAdmins(
                    flow=flow,
                    translator=translator,
                    guild_id=guild_id,
                    protection_service=protection_service,
                )
            )

            self.add_item(
                DeleteForAdmins(
                    flow=flow,
                    translator=translator,
                    guild_id=guild_id,
                    protection_service=protection_service,
                )
            )
