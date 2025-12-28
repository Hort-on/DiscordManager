import discord
from database.db_factory.db_scenario_factory import DBScenarioFactory
from modules.logger.logger import Logger
from utils.format_the_result import FormatResult
from utils.messages import GENERAL_MSGS, DB_MSGS


class FinishingConfiguration:
    def __init__(
            self,
            parent,
            db: DBScenarioFactory,
            logger: Logger
    ):

        self.parent = parent
        self.db = db
        self.logger = logger

    async def finishing_configuration(self, interaction: discord.Interaction) -> None:
        try:
            await self.db.write_data(
                interaction.guild.id,
                'settings',
                {key.replace('_enabled', ''): value for key, value in self.parent.config.items()}
            )
        except Exception as e:
            await self.logger.error(DB_MSGS.get('failure_write_msg'), exc=e)
            return

        if not self.parent.found_users:
            await self.send_the_result(interaction)

        await self.users_procedure(interaction)

    async def users_procedure(self, interaction) -> None:
        for member in self.parent.found_users:
            try:
               await self.db.write_data(
                    interaction.guild.id,
                    "super_users",
                    {"user_id": member.id
                     })

            except Exception as e:
                await self.logger.error(DB_MSGS.get('failure_write_msg'), exc=e)
                return

        await self.send_the_result(interaction)

    async def send_the_result(self, interaction: discord.Interaction) -> None:

        summary_result = FormatResult.format_the_result(parent=self.parent, interaction=interaction, start=True)

        await interaction.edit_original_response(
            content=GENERAL_MSGS.get('configuration_done_msg') + f'\n\n{summary_result}\n\n'
        )
