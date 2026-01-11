import discord

from modules.birthdays.birthday_repo import BirthdayManager
from modules.buttons.buttons_for_admins.birthday_button.add_birthday import AddBirthdayButton
from modules.buttons.buttons_for_admins.birthday_button.delete_birthday import \
    DeleteBirthdayButton
from modules.buttons.back import BackButton
from modules.management.button_manager import ButtonManager


class BirthdayMenuView(discord.ui.View):
    def __init__(
            self,
            guild_id,
            birthday_manager: BirthdayManager,
    ):
        super().__init__(timeout=60)

        self.add_item(AddBirthdayButton(birthday_manager))
        self.add_item(DeleteBirthdayButton(birthday_manager))
        self.add_item(BackButton(lambda: ButtonManager(guild_id=guild_id)))
