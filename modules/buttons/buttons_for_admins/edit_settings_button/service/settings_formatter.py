import discord
from database.data_base_model import DB
from utils.format_the_result import FormatResult
from utils.messages import GENERAL_MESSAGES as GM


class SettingsFormatter:
    def __init__(self):
        self.db = DB()
        self.config = {}

    async def format_settings(self, interaction: discord.Interaction) -> None:
        self.config = await self.db.get_data(
            interaction.guild_id,
            'settings'
        )

        summary_result = FormatResult.format_the_result(parent=self, interaction=interaction, start=False)

        await interaction.edit_original_response(
            content=GM.get('edit_settings_msg') + f'\n\n{summary_result}\n\n'
        )
