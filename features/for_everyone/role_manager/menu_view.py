from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.for_everyone.role_manager.buttons import AddRoleButton, RemoveRoleButton
from ui.buttons.back_button import BackButton

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_everyone.role_manager.flow import RoleManagerFlow
    from general_services.translator.translator import Translator


class RoleManagerView(discord.ui.View):
    def __init__(
        self,
        navigator: Navigator,
        flow: RoleManagerFlow,
        translator: Translator,
        guild_id: int,
    ):
        super().__init__(timeout=60)

        self.add_item(
            AddRoleButton(
                navigator=navigator, flow=flow, translator=translator, guild_id=guild_id
            )
        )

        self.add_item(
            RemoveRoleButton(
                navigator=navigator, flow=flow, translator=translator, guild_id=guild_id
            )
        )

        self.add_item(
            BackButton(navigator=navigator, translator=translator, guild_id=guild_id)
        )
