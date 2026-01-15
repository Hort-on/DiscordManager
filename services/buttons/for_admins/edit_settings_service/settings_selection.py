import discord

from modules.buttons.others.back import BackButton
from modules.buttons.views.for_admins.admin_menu import AdminMenuView
from services.buttons.for_admins.edit_settings_service.choice_handler import ChoiceHandler
from services.factories.db_factory.db_scenario_factory import DBScenarioFactory
from services.utils.option_list import SETTINGS_OPTIONS
from services.utils.messages import SYSTEM_MSGS as SM


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

        self.choice_handler = ChoiceHandler(db_factory)

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
            guild_id: int,
            user_id: int,
            db_factory: DBScenarioFactory
    ):
        super().__init__(timeout=None)
        self.add_item(SettingSelector(db_factory))
        self.add_item(BackButton(
            view_factory=lambda: AdminMenuView(
                guild_id=guild_id,
                user_id=user_id
            )))
