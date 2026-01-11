import discord

from database.settings_storage.settings_storage import SettingsStorage
from services.button_services.edit_settings_service.SettingsSelectionService import SettingSelectorView
from services.button_services.edit_settings_service.SettingsFormaterService import SettingsFormatter
from services.factories.db_factory.db_scenario_factory import DBScenarioFactory


class EditSettingsButton(discord.ui.Button):
    def __init__(
            self,
            db_factory: DBScenarioFactory,
            settings: SettingsStorage
    ):
        super().__init__(
            label="Edit settings",
            style=discord.ButtonStyle.green
        )

        self.db_factory = db_factory

        self.settings_formatter = SettingsFormatter(settings)

    async def callback(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()
        summary = await self.settings_formatter.format_settings(interaction)

        view = SettingSelectorView(self.db_factory)

        await interaction.edit_original_response(
            content=summary,
            view=view,
        )
