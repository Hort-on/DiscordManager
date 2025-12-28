import discord

from database.db_factory.db_scenario_factory import DBScenarioFactory
from modules.logger.logger import Logger
from utils.format_the_result import FormatResult
from utils.messages import GENERAL_MSGS as GM


class SettingsFormatter:
    def __init__(self, db: DBScenarioFactory, logger: Logger):
        self.db = db
        self.logger = logger
        self.config = {}

    async def format_settings(self, interaction: discord.Interaction) -> None:
        scenario_get_data = self.db.for_fetch_all(
            self.logger,
            interaction.guild_id,
            'settings'
        )

        summary_result = FormatResult.format_the_result(parent=self, interaction=interaction, start=False)

        await interaction.edit_original_response(
            content=GM.get('config_edit_msg') + f'\n\n{summary_result}\n\n'
        )
