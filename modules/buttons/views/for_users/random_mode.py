import discord

from modules.buttons.others.back import BackButton
from modules.buttons.for_users.randomizer.random_number import RandomNumButton
from modules.buttons.for_users.randomizer.random_team_by_channel import RandomTeamByChannel
from modules.buttons.for_users.randomizer.random_team_by_msg import RandomTeamByMsg
from modules.buttons.for_users.randomizer.random_word import RandomWordButton

from modules.management.button_manager import ButtonManager


class RandomModeView(discord.ui.View):
    def __init__(self, guild_id: int, user_id: int):
        super().__init__(timeout=60)
        self.add_item(RandomNumButton())
        self.add_item(RandomWordButton())
        self.add_item(RandomTeamByMsg())
        self.add_item(RandomTeamByChannel())
        self.add_item(BackButton(
            view_factory=lambda: ButtonManager(
                guild_id=guild_id, user_id=user_id
            ))
        )
