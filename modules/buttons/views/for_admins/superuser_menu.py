import discord

from database.settings_storage.settings import SettingsStorage
from modules.birthdays.birthday_repo import BirthdayManager

from modules.buttons.for_admins.superusers_button.add_superuser import AddSuperuserButton
from modules.buttons.for_admins.superusers_button.delete_superuser import DeleteSuperusersButton
from modules.buttons.for_admins.superusers_button.list_of_superusers import SuperusersListButton
from modules.buttons.others.back import BackButton
from modules.buttons.views.for_admins.admin_menu import AdminMenuView

from services.factories.db_factory.db_scenario_factory import DBFactory


class SuperusersMenuView(discord.ui.View):
    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBFactory,
            birthday_manager: BirthdayManager,
            guild_id: int,
            user_id: int
    ):
        super().__init__(timeout=60)

        self.add_item(AddSuperuserButton())
        self.add_item(DeleteSuperusersButton(settings=settings, db_factory=db_factory))
        self.add_item(SuperusersListButton(settings=settings, db_factory=db_factory))

        self.add_item(BackButton(back_view=lambda: AdminMenuView(
            settings=settings,
            db_factory=db_factory,
            birthday_manager=birthday_manager,
            guild_id=guild_id,
            user_id=user_id
        )))
