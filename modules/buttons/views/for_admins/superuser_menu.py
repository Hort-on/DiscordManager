import discord

from database.settings_storage.settings import SettingsStorage

from modules.buttons.for_admins.superusers_button.add_superuser import AddSuperuserButton
from modules.buttons.for_admins.superusers_button.list_of_superusers import SuperusersListButton
from modules.buttons.others.back import BackButton
from modules.buttons.views.for_admins.admin_menu import AdminMenuView

from services.factories.db_factory.db_scenario_factory import DBScenarioFactory


class SuperusersMenuView(discord.ui.View):
    def __init__(
            self,
            guild_id: int,
            user_id: int,
            settings: SettingsStorage,
            db_factory: DBScenarioFactory
    ):
        super().__init__(timeout=60)

        self.add_item(AddSuperuserButton())
        self.add_item(DeleteSuperuserButton())
        self.add_item(SuperusersListButton(settings=settings, db_factory=db_factory))

        self.add_item(BackButton(
            view_factory=lambda: AdminMenuView(guild_id=guild_id, user_id=user_id)
        ))
