from __future__ import annotations

import discord

from modules.buttons.for_admins.delete_message_buttons.buttons import DeleteAnyMessageButton, DeleteUserMessageButton
from modules.buttons.other_buttons.back import BackButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.buttons.navigator import Navigator


class DeleteMsgMenuView(discord.ui.View):
    def __init__(self, navigator: Navigator):
        super().__init__(timeout=60)

        self.add_item(DeleteAnyMessageButton())
        self.add_item(DeleteUserMessageButton())
        self.add_item(BackButton(
            target='admin_menu',
            navigator=navigator
        ))
