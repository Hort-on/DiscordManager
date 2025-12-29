import discord

from utils.format_the_result import FormatResult
from utils.messages import GENERAL_MSGS as GM


class SettingsFormatter:
    def __init__(self):
        self.config = {}

    async def format_settings(self, interaction: discord.Interaction) -> None:
        summary_result = FormatResult.format_the_result(
            parent=self,
            interaction=interaction,
            start=False
        )

        await interaction.edit_original_response(
            content=GM.get('config_edit_msg') + f'\n\n{summary_result}\n\n'
        )
