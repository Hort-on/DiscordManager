import discord

from factories.db_factory import DBScenarioFactory
from database.settings_storage.settings_storage import SettingsStorage

from utils.format_result.esult_scenarios_factory import ResultFactory
from utils.messages import GENERAL_MSGS as GM


class SettingsFormatter:
    def __init__(
            self,
            db_factory: DBScenarioFactory,
            settings: SettingsStorage
    ):

        self.settings = settings
        self.db_factory = db_factory

    async def format_settings(self, interaction: discord.Interaction) -> None:
        scenario = ResultFactory.for_settings_edit(self.db_factory, self.settings)
        summary_result = scenario.format_the_result(
            parent=self,
            interaction=interaction
        )

        await interaction.edit_original_response(
            content=GM.get('config_edit_msg') + f'\n\n{summary_result}\n\n'
        )
