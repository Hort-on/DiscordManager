from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.navigator import Navigator

import discord

from modules.buttons.for_admins.delete_message_buttons.buttons import DeleteAnyMessageButton, DeleteUserMessageButton
from modules.buttons.other_buttons.back import BackButton


class DeleteMsgMenuView(discord.ui.View):
    def __init__(self, navigator: Navigator):
        super().__init__(timeout=60)

        self.add_item(DeleteAnyMessageButton(navigator=navigator))
        self.add_item(DeleteUserMessageButton(navigator=navigator))
        self.add_item(BackButton(navigator=navigator))
