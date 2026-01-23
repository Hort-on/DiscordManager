from __future__ import annotations

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.buttons.for_admins.delete_message_buttons.menu_view import DeleteMsgMenuView

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.buttons.navigator import Navigator


class DeleteMsgMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='Delete message',
            style=discord.ButtonStyle.blurple
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        view = DeleteMsgMenuView(navigator=self.navigator)
        await interaction.edit_original_response(view=view)
