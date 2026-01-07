import discord

from services.factories import DBScenarioFactory
from database.settings_storage.settings_storage import SettingsStorage

from services.button_services.edit_settings_service.SettingsSelectionService import SettingSelectorView
from services.button_services.edit_settings_service.SettingsFormaterService import SettingsFormatter


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
        self.settings = settings

        self.settings_formatter = SettingsFormatter(self.db_factory, self.settings)

    async def callback(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()
        summary = self.settings_formatter.format_settings(interaction)

        view = SettingSelectorView(self.db_factory)

        await interaction.response.send_message(
            summary,
            view=view,
            ephemeral=True
        )
