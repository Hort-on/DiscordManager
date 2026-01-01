import discord

from database.db_factory.db_scenario_factory import DBScenarioFactory
from modules.configuration.starting_configuration import ConfigurationView
from utils.messages import EDIT_CONFIG_MSGS as ECM
from modules.buttons.buttons_for_admins.edit_settings_button.service.setting_selection import SettingSelectorView


class BaseScenario:
    async def yes_no_proceed(self, interaction: discord.Interaction, value: bool):
        raise NotImplementedError


class StartConfigScenario(BaseScenario):
    def __init__(
            self,
            parent: ConfigurationView,
            config_key: str,
            on_decline_callback
    ):
        self.parent = parent
        self.config_key = config_key
        self.on_decline_callback = on_decline_callback

    async def yes_no_proceed(
            self,
            interaction: discord.Interaction,
            value: bool
    ) -> None:

        if self.config_key is not None:
            self.parent.config[self.config_key] = value

        if not value and self.on_decline_callback:
            await self.on_decline_callback(interaction)
            return

        await self.parent.next_step(interaction)


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
