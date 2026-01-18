import discord

from database.settings_storage.settings import SettingsStorage

from modules.birthdays.birthday_repo import BirthdayManager
from modules.buttons.views.for_admins.admin_menu import AdminMenuView

from services.buttons.protection.admin_buttons_protection import FirewallButton
from services.factories.db_factory.db_scenario_factory import DBFactory


class AdminMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBFactory,
            birthday_manager: BirthdayManager
    ):
        super().__init__(
            label='Admin menu',
            style=discord.ButtonStyle.secondary
        )
        self.settings = settings
        self.db_factory = db_factory,
        self.birthday_manager = birthday_manager

    async def callback(self, interaction: discord.Interaction):
        view = AdminMenuView(
            guild_id=interaction.guild_id,
            user_id=interaction.user.id,
            settings=self.settings,
            db_factory=self.db_factory,
            birthday_manager=self.birthday_manager
        )

        await interaction.edit_original_response(
            view=view
        )
