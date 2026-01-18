import discord

from database.settings_storage.settings import SettingsStorage

from modules.birthdays.birthday_repo import BirthdayManager
from modules.buttons.others.back import BackButton
from modules.buttons.for_users.randomizer.random_number import RandomNumButton
from modules.buttons.for_users.randomizer.random_team_by_channel import RandomTeamByChannel
from modules.buttons.for_users.randomizer.random_team_by_msg import RandomTeamByMsg
from modules.buttons.for_users.randomizer.random_word import RandomWordButton
from modules.management.button_manager import ButtonManager

from services.factories.db_factory.db_scenario_factory import DBFactory


class RandomModeView(discord.ui.View):
    def __init__(self,
                 settings: SettingsStorage,
                 db_factory: DBFactory,
                 birthday_manager: BirthdayManager,
                 guild_id: int,
                 user_id: int
                 ):
        super().__init__(timeout=60)
        self.add_item(RandomNumButton())
        self.add_item(RandomWordButton())
        self.add_item(RandomTeamByMsg())
        self.add_item(RandomTeamByChannel())
        self.add_item(BackButton(
            back_view=lambda: ButtonManager(
                settings=settings,
                db_factory=db_factory,
                birthday_manager=birthday_manager,
                guild_id=guild_id,
                user_id=user_id
            ))
        )
