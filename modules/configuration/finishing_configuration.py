import discord
from database.data_base_model import DB
from utils.format_the_result import FormatResult
from utils.messages import GENERAL_MESSAGES as GM


class FinishingConfiguration:
    def __init__(self, parent):
        self.parent = parent
        self.db = DB()


    async def finishing_configuration(self, interaction: discord.Interaction) -> None:
        try:
            await self.db.write_data(
                interaction.guild.id,
                'settings',
                {key.replace('_enabled', ''): value for key, value in self.parent.config.items()}
            )
        except Exception as e:
            print(f"[DB ERROR] Failed to write config to the db: {e}")

        if self.parent.found_users:
            await self.users_procedure(interaction)
        else:
            await self.send_the_result(interaction)

    async def users_procedure(self, interaction) -> None:
        for member in self.parent.found_users:
            try:
               await self.db.write_data(
                    interaction.guild.id,
                    "super_users",
                    {"user_id": member.id
                     })
            except Exception as e:
                await interaction.edit_original_response(
                    content="❌ Failed to save configuration. Please try again."
                )
                return

        await self.send_the_result(interaction)

    async def send_the_result(self, interaction: discord.Interaction) -> None:

        summary_result = FormatResult.format_the_result(parent=self.parent, interaction=interaction, start=True)

        await interaction.edit_original_response(
            content=GM.get('configuration_done') + f'\n\n{summary_result}\n\n' + GM.get('configuration_done_2')
        )
