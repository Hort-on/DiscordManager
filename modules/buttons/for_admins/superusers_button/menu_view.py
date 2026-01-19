import discord

from modules.buttons.for_admins.superusers_button.buttons import (
    AddSuperuserButton,
    DeleteSuperusersButton,
    SuperusersListButton
)

from modules.buttons.other_buttons.back import BackButton
from modules.buttons.for_admins.admin_menu_view import AdminMenuView


class SuperusersMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    def prepare(self, guild_id: int, user_id: int):
        self.add_item(AddSuperuserButton())
        self.add_item(DeleteSuperusersButton())
        self.add_item(SuperusersListButton())

        self.add_item(BackButton(back_view=lambda: AdminMenuView().prepare(
            guild_id=guild_id,
            user_id=user_id
        )))

        return self
