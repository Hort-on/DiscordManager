from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.for_admins.superusers.buttons import (
    AddSuperuserButton,
    DeleteSuperusersButton,
    SuperusersListButton
)

from ui.buttons.back_button import BackButton

if TYPE_CHECKING:
    from core.navigator import Navigator
    from features.for_admins.superusers.flow import SuperusersFlow
    from ui.button_protection.button_protection_service import ButtonProtectionService


class SuperusersMenuView(discord.ui.View):
    def __init__(
            self,
            navigator: Navigator,
            buttons_protection: ButtonProtectionService,
            flow: SuperusersFlow
    ):
        super().__init__(timeout=60)

        self.add_item(AddSuperuserButton(
            buttons_protection=buttons_protection,
            flow=flow
        ))

        self.add_item(DeleteSuperusersButton(
            buttons_protection=buttons_protection,
            flow=flow
        ))

        self.add_item(SuperusersListButton(
            buttons_protection=buttons_protection,
            flow=flow
        ))

        self.add_item(BackButton(navigator=navigator))
