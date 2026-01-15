import discord

from database.settings_storage.settings import SettingsStorage

from services.utils.format_result.scenarios_factory import ResultFactory
from services.utils.messages import GENERAL_MSGS as GM


class SettingsFormatter:
    def __init__(
            self,
            settings: SettingsStorage
    ):

        self.settings = settings

    async def format_settings(self, interaction: discord.Interaction) -> None:
        scenario = ResultFactory.for_settings_edit(settings=self.settings)
        summary_result = scenario.format_the_result(
            parent=self,
            interaction=interaction
        )

        await interaction.edit_original_response(
            content=GM.get('config_edit_msg') + f'\n\n{summary_result}\n\n'
        )
