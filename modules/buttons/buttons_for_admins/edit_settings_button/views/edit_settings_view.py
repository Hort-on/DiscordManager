import discord

from database.db_factory.db_scenario_factory import DBScenarioFactory
from modules.buttons.buttons_for_admins.edit_settings_button.service.setting_selection import SettingSelectorView
from modules.buttons.buttons_for_admins.edit_settings_button.service.settings_formatter import SettingsFormatter
from modules.logger.logger import Logger


class EditSettingsButton(discord.ui.Button):
    def __init__(
            self,
            db_factory: DBScenarioFactory
    ):
        super().__init__(
            label="Edit settings",
            style=discord.ButtonStyle.green
        )

        self.db_factory = db_factory

        self.settings_formatter = SettingsFormatter()

    async def callback(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()
        summary = self.settings_formatter.format_settings(interaction)

        view = SettingSelectorView(self.db_factory)

        await interaction.response.send_message(
            summary,
            view=view,
            ephemeral=True
        )
