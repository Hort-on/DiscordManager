import discord

from services.factories import DBScenarioFactory

from services.utils.messages import EDIT_CONFIG_MSGS as ECM

from services.button_services.edit_settings_service.SettingsSelectionService import SettingSelectorView


class BaseScenario:
    async def yes_no_proceed(self, interaction: discord.Interaction, value: bool):
        raise NotImplementedError


class ConfirmationScenario(BaseScenario):
    def __init__(
            self,
            db_factory: DBScenarioFactory,
            config_key: str
    ):
        self.db_factory = db_factory
        self.config_key = config_key

    async def yes_no_proceed(
            self,
            interaction: discord.Interaction,
            value: bool
    ) -> None:

        write_data_scenario = self.db_factory.for_write_data(
            interaction.guild.id,
            'settings',
            {self.config_key: value}
        )

        result = await write_data_scenario.db_proceed()
        if not result:
            await interaction.message.edit(
                content=ECM.get('failure_edit_msg'),
                view=SettingSelectorView(self.db_factory)
            )
            return

        await interaction.message.edit(
            content=ECM.get('success_edit_msg'),
            view=SettingSelectorView(self.db_factory)
        )
