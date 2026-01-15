import discord

from modules.birthdays.birthday_repo import BirthdayManager
from modules.buttons.for_admins.birthday_buttons.add_birthday import AddBirthdayButton
from modules.buttons.for_admins.birthday_buttons.delete_birthday import \
    DeleteBirthdayButton
from modules.buttons.others.back import BackButton
from modules.buttons.views.for_admins.admin_menu import AdminMenuView


class BirthdayMenuView(discord.ui.View):
    def __init__(
            self,
            guild_id,
            user_id: int,
            birthday_manager: BirthdayManager,
    ):
        super().__init__(timeout=60)

        self.add_item(AddBirthdayButton(birthday_manager))
        self.add_item(DeleteBirthdayButton(birthday_manager))
        self.add_item(BackButton(view_factory=lambda: AdminMenuView(
            guild_id=guild_id,
            user_id=user_id
        )))
