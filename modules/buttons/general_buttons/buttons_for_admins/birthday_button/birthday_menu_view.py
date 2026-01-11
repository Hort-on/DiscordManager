import discord

from modules.birthdays.birthday_repo import BirthdayManager
from modules.buttons.general_buttons.buttons_for_admins.birthday_button.add_birthday_button import AddBirthdayButton
from modules.buttons.general_buttons.buttons_for_admins.birthday_button.delete_birthday_button import \
    DeleteBirthdayButton
from modules.buttons.general_buttons.back_button import BackButton
from modules.management.management import ButtonManager


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
