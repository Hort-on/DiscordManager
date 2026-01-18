import discord

from database.settings_storage.settings import SettingsStorage

from modules.birthdays.birthday_repo import BirthdayManager

from services.buttons.for_admins.edit_settings_service.settings_selection import SettingSelectorView
from services.factories.db_factory.db_scenario_factory import DBFactory
from services.utils.messages import EDIT_CONFIG_MSGS as ECM


class BaseScenario:
    async def yes_no_proceed(self, interaction: discord.Interaction, value: bool):
        raise NotImplementedError


class ConfirmationScenario(BaseScenario):
    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBFactory,
            birthday_manager: BirthdayManager,
            config_key: str
    ):
        self.settings = settings
        self.db_factory = db_factory
        self.birthday_manager = birthday_manager
        self.config_key = config_key

    async def yes_no_proceed(
            self,
            interaction: discord.Interaction,
            value: bool
    ) -> None:

        write_data_scenario = self.db_factory.for_write_data(
            guild_id=interaction.guild.id,
            table_name='settings',
            data={self.config_key: value}
        )

        result = await write_data_scenario.db_proceed()
        if not result:
            await interaction.edit_original_response(
                content=ECM.get('failure_edit_msg' if not result else 'success_edit_msg'),
                view=SettingSelectorView(
                    settings=self.settings,
                    db_factory=self.db_factory,
                    birthday_manager=self.birthday_manager,
                    guild_id=interaction.guild_id,
                    user_id=interaction.user.id
                )
            )
