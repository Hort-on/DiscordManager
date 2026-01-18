import discord

from database.settings_storage.settings import SettingsStorage

from modules.birthdays.birthday_repo import BirthdayManager
from modules.buttons.views.for_users.random_mode import RandomModeView

from services.buttons.protection.admin_buttons_protection import FirewallButton
from services.factories.db_factory.db_scenario_factory import DBFactory


class RandomMenuButton(FirewallButton):
    scope = 'user'

    def __init__(self,
                 settings: SettingsStorage,
                 db_factory: DBFactory,
                 birthday_manager: BirthdayManager
                 ):
        super().__init__(
            label='🎲 Randomizer',
            style=discord.ButtonStyle.blurple
        )
        self.settings = settings
        self.db_factory = db_factory
        self.birthday_manager = birthday_manager

    async def on_click(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()

        await interaction.edit_original_response(
            content='Choose randomizer mode:',
            view=RandomModeView(
                settings=self.settings,
                db_factory=self.db_factory,
                birthday_manager=self.birthday_manager,
                guild_id=interaction.guild_id,
                user_id=interaction.user.id
            )
        )
