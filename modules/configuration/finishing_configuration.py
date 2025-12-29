import discord

from database.db_factory.db_scenario_factory import DBScenarioFactory

from utils.format_the_result import FormatResult
from utils.messages import GENERAL_MSGS, SYSTEM_MSGS


class FinishingConfiguration:
    def __init__(
            self,
            parent,
            db_factory: DBScenarioFactory,
    ):

        self.parent = parent
        self.db_factory = db_factory

    async def finishing_configuration(self, interaction: discord.Interaction) -> None:
        write_data_scenario = self.db_factory.for_write_data(
            interaction.guild.id,
            'settings',
            {key.replace('_enabled', ''): value for key, value in self.parent.config.items()}
        )

        result = await write_data_scenario.db_proceed()
        if not result:
            await interaction.edit_original_response(
                content=SYSTEM_MSGS.get('failure_msg')
            )
            return

        if not self.parent.found_users:
            await self.send_the_result(interaction)

        await self.superusers_procedure(interaction)

    async def superusers_procedure(self, interaction: discord.Interaction) -> None:
        user_ids = [member.id for member in self.parent.found_users]

        write_data_scenario = self.db_factory.for_write_user(
            interaction.guild.id,
            "super_users",
            user_ids
        )

        result = await write_data_scenario.db_proceed()
        if not result:
            await interaction.edit_original_response(
                content=SYSTEM_MSGS.get('failure_msg')
            )
            return

        await self.send_the_result(interaction)

    async def send_the_result(self, interaction: discord.Interaction) -> None:

        summary_result = FormatResult.format_the_result(parent=self.parent, interaction=interaction, start=True)

        await interaction.edit_original_response(
            content=GENERAL_MSGS.get('configuration_done_msg') + f'\n\n{summary_result}\n\n'
        )
