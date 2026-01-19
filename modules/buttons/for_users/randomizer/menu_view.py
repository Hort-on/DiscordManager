import discord

from modules.buttons.for_users.randomizer.buttons import (
    RandomNumButton,
    RandomWordButton,
    RandomTeamByMsg,
    RandomTeamByChannel
)

from modules.buttons.other_buttons.back import BackButton
from modules.buttons.main_button_view import MainButtonView


class RandomModeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    def prepare(self, guild_id: int, user_id: int):
        self.add_item(RandomNumButton())
        self.add_item(RandomWordButton())
        self.add_item(RandomTeamByMsg())
        self.add_item(RandomTeamByChannel())
        self.add_item(BackButton(
            back_view=lambda: MainButtonView().prepare(
                guild_id=guild_id,
                user_id=user_id
            )))

        return self
