from __future__ import annotations

import discord

from modules.buttons.for_admins.edit_settings_buttons.services import SettingSelectorView

from services.factories.db_factory.db_scenario_factory import DBFactory
from services.utils.messages import EDIT_CONFIG_MSGS as ECM

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.buttons.navigator import Navigator
    from services.yes_no_service.yes_no_factory import YesNoViewFactory


class BaseScenario:
    async def yes_no_proceed(self, interaction: discord.Interaction, value: bool):
        raise NotImplementedError


class ConfirmationScenario(BaseScenario):
    def __init__(
            self,
            db_factory: DBFactory,
            navigator: Navigator,
            yes_no_factory: YesNoViewFactory,
            config_key: str
    ):

        self.db_factory = db_factory
        self.nafigator = navigator
        self.yes_no_factory = yes_no_factory
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
                    navigator=self.nafigator,
                    db_factory=self.db_factory,
                    yes_no_factory=self.yes_no_factory
                ))


class ForBirthdayScenario(BaseScenario):
    async def yes_no_proceed(
            self,
            interaction: discord.Interaction,
            value: bool
    ) -> None:
        if not value:
            return

        await interaction.response.send_modal()
