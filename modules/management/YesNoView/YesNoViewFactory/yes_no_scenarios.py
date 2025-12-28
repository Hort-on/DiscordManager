import discord

from database.data_base_model import DB
from database.db_factory.db_scenario_factory import DBScenarioFactory
from utils.messages import EDIT_CONFIG_MESSAGES as ECM
from modules.buttons.buttons_for_admins.edit_settings_button.service.setting_selection import SettingSelectorView


class BaseScenario:
    async def yes_no_proceed(self, interaction: discord.Interaction, **kwargs):
        raise NotImplementedError


class StartConfigScenario(BaseScenario):
    def __init__(self, parent, config_key, on_decline_callback):
        self.parent = parent
        self.config_key = config_key
        self.on_decline_callback = on_decline_callback

    async def yes_no_proceed(self, interaction: discord.Interaction, **kwargs):
        value: bool = kwargs.get('value')

        if self.config_key is not None:
            self.parent.config[self.config_key] = value

        if not value and self.on_decline_callback:
            await self.on_decline_callback(interaction)
            return

        await self.parent.next_step(interaction)


class ConfirmationScenario(BaseScenario):
    def __init__(self, db: DBScenarioFactory, config_key):
        self.db = db
        self.config_key =  config_key

    async def yes_no_proceed(self, interaction, **kwargs):
        value: bool = kwargs.get('value')
        try:
            await self.db.write_data(
                interaction.guild.id,
                'settings',
                {self.config_key: value}
            )

            await interaction.message.edit(
                content=ECM.get('success_edit_msg'),
                view=SettingSelectorView(self.db)
            )

        except Exception as e:
            print('[DB ERROR]', e)
            await interaction.message.edit(
                content=ECM.get('failure_edit_msg'),
                view=SettingSelectorView(self.db)
            )
