from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator

import discord

from modules.buttons.other_buttons.back import BackButton
from modules.buttons.for_admins.edit_settings_buttons.buttons import MainSettingsButton


class SettingsMenuView(discord.ui.View):
    def __init__(self, navigator: Navigator):
        super().__init__(timeout=60)

        self.add_item(MainSettingsButton(navigator=navigator))
        self.add_item(BackButton(navigator=navigator))
