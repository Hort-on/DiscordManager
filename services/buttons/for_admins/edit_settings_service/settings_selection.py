import discord

from database.settings_storage.settings import SettingsStorage

from modules.birthdays.birthday_repo import BirthdayManager
from modules.buttons.others.back import BackButton
from modules.buttons.views.for_admins.admin_menu import AdminMenuView

from services.buttons.for_admins.edit_settings_service.choice_handler import ChoiceHandler
from services.factories.db_factory.db_scenario_factory import DBFactory
from services.utils.option_list import SETTINGS_OPTIONS
from services.utils.messages import SYSTEM_MSGS as SM


class SettingSelector(discord.ui.Select):
    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBFactory,
            birthday_manager: BirthdayManager
    ):
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

        self.choice_handler = ChoiceHandler(
            settings=settings,
            db_factory=db_factory,
            birthday_manager=birthday_manager
        )

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
            interaction=interaction,
            option_type=option_type,
            config_key=config_key
        )


class SettingSelectorView(discord.ui.View):
    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBFactory,
            birthday_manager: BirthdayManager,
            guild_id: int,
            user_id: int
    ):
        super().__init__(timeout=None)
        self.add_item(SettingSelector(
            settings=settings,
            db_factory=db_factory,
            birthday_manager=birthday_manager
        ))
        self.add_item(BackButton(
            back_view=lambda: AdminMenuView(
                settings=settings,
                db_factory=db_factory,
                birthday_manager=birthday_manager,
                guild_id=guild_id,
                user_id=user_id
            )))
