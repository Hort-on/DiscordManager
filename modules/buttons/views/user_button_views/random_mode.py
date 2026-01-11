import discord

from modules.buttons.back import BackButton
from modules.buttons.buttons_for_users.randomizer_buttons.random_number import RandomNumButton
from modules.buttons.buttons_for_users.randomizer_buttons.random_team_by_channel import RandomTeamByChannel
from modules.buttons.buttons_for_users.randomizer_buttons.random_team_by_msg import RandomTeamByMsg
from modules.buttons.buttons_for_users.randomizer_buttons.random_word import RandomWordButton

from modules.management.button_manager import ButtonManager


class RandomModeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(RandomNumButton())
        self.add_item(RandomWordButton())
        self.add_item(RandomTeamByMsg())
        self.add_item(RandomTeamByChannel())
        self.add_item(BackButton(lambda: ButtonManager()))
