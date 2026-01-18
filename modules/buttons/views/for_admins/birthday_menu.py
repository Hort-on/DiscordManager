import discord

from database.settings_storage.settings import SettingsStorage

from modules.birthdays.birthday_repo import BirthdayManager
from modules.buttons.for_admins.birthday_buttons.add_birthday import AddBirthdayButton
from modules.buttons.for_admins.birthday_buttons.delete_birthday import \
    DeleteBirthdayButton
from modules.buttons.others.back import BackButton
from modules.buttons.views.for_admins.admin_menu import AdminMenuView

from services.factories.db_factory.db_scenario_factory import DBFactory


class BirthdayMenuView(discord.ui.View):
    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBFactory,
            birthday_manager: BirthdayManager,
            guild_id: int,
            user_id: int
    ):
        super().__init__(timeout=60)

        self.add_item(AddBirthdayButton(birthday_manager))
        self.add_item(DeleteBirthdayButton(birthday_manager))
        self.add_item(BackButton(back_view=lambda: AdminMenuView(
            settings=settings,
            db_factory=db_factory,
            birthday_manager=birthday_manager,
            guild_id=guild_id,
            user_id=user_id
        )))
