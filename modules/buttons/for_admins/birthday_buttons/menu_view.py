import discord

from modules.buttons.for_admins.birthday_buttons.buttons import AddBirthdayButton, DeleteBirthdayButton
from modules.buttons.other_buttons.back import BackButton
from modules.buttons.for_admins.admin_menu_view import AdminMenuView


class BirthdayMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    def prepare(self, guild_id: int, user_id: int):
        self.add_item(AddBirthdayButton())
        self.add_item(DeleteBirthdayButton())
        self.add_item(BackButton(back_view=lambda: AdminMenuView().prepare(
            guild_id=guild_id,
            user_id=user_id
        )))

        return self
