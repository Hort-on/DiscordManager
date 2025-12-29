import discord

from database.db_factory.db_scenario_factory import DBScenarioFactory
from modules.buttons.buttons_for_admins.edit_settings_button.service.choice_handler import ChoiceHandler
from utils.option_list import SETTINGS_OPTIONS
from utils.messages import SYSTEM_MSGS as SM


class SettingSelector(discord.ui.Select):
    def __init__(self, db_factory: DBScenarioFactory):
        super().__init__(
            placeholder="Please select a setting to edit...",
            options=[
                discord.SelectOption(
                    label=key.replace("_", " ").title(),
                    value=key
                )
                for key in SETTINGS_OPTIONS.keys()
            ],
            min_values=1,
            max_values=1
        )

        self.db_factory = db_factory

        self.choice_handler = ChoiceHandler(self.db_factory)

    async def callback(
            self,
            interaction: discord.Interaction
    ) -> None:

        config_key = self.values[0]
        option_type = SETTINGS_OPTIONS.get(config_key)

        if not option_type:
            await interaction.edit_original_response(
                content=SM.get('failure_msg')
            )
            return

        await self.choice_handler.choice_procedure(
            interaction,
            option_type,
            config_key
        )


class SettingSelectorView(discord.ui.View):
    def __init__(
            self,
            db_factory: DBScenarioFactory
    ):
        super().__init__(timeout=None)
        self.db_factory = db_factory
        self.add_item(SettingSelector(self.db_factory))
