import discord

from core.bot_container import AppContainer
from core.main import BotController

from modules.buttons.for_admins.edit_settings_buttons.services import SettingSelectorView

from services.utils.messages import EDIT_CONFIG_MSGS as ECM


class BaseScenario:
    async def yes_no_proceed(self, interaction: discord.Interaction, value: bool):
        raise NotImplementedError


class ConfirmationScenario(BaseScenario):
    def __init__(self, config_key: str):
        controller: BotController = AppContainer.get()

        self.db_factory = controller.db_factory
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
                view=SettingSelectorView().prepare(
                    guild_id=interaction.guild_id,
                    user_id=interaction.user.id
                )
            )
