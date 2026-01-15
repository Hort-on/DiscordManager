import discord

from database.settings_storage.settings import SettingsStorage
from modules.buttons.views.for_admins.superuser_menu import SuperusersMenuView

from services.buttons.protection.admin_buttons_protection import FirewallButton
from services.factories.db_factory.db_scenario_factory import DBScenarioFactory


class SuperusersMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBScenarioFactory
    ):
        super().__init__(
            label='Superusers management',
            style=discord.ButtonStyle.green
        )
        self.settings = settings
        self.db_factory = db_factory

    async def on_click(self, interaction: discord.Interaction) -> None:
        view = SuperusersMenuView(
            guild_id=interaction.guild_id,
            user_id=interaction.user.id,
            settings=self.settings,
            db_factory=self.db_factory
        )
        await interaction.edit_original_response(view=view)
