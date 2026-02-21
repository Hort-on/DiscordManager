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
    from features.for_admins.superusers.services import SuperusersService
    from features.for_admins.superusers.formatter import SuperusersFormatter


class SuperusersMenuView(discord.ui.View):
    def __init__(
            self,
            navigator: Navigator,
            superusers_service: SuperusersService,
            formatter: SuperusersFormatter
    ):
        super().__init__(timeout=60)

        self.add_item(AddSuperuserButton(
            navigator=navigator,
            superusers_service=superusers_service,
            formatter=formatter
        ))
        self.add_item(DeleteSuperusersButton(
            navigator=navigator,
            superusers_service=superusers_service,
            formatter=formatter
        ))
        self.add_item(SuperusersListButton(
            formatter=formatter
        ))
        self.add_item(BackButton(navigator=navigator))
