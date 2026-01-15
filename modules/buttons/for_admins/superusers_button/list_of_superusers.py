import discord

from database.settings_storage.settings import SettingsStorage

from services.buttons.for_admins.superusers.get_superusers_list import GetSuperusersList
from services.buttons.protection.admin_buttons_protection import FirewallButton
from services.factories.db_factory.db_scenario_factory import DBScenarioFactory


class SuperusersListButton(FirewallButton):
    scope = "admin"

    def __init__(self, settings: SettingsStorage, db_factory: DBScenarioFactory):
        super().__init__(
            label="Show current superusers",
            style=discord.ButtonStyle.green,
        )
        self.service = GetSuperusersList(settings=settings, db_factory=db_factory)

    async def on_click(self, interaction: discord.Interaction):
        result = self.service.get_display(guild=interaction.guild)
        await interaction.edit_original_response(content=result)

