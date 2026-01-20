import discord

from modules.buttons.for_users.role_manager.buttons import AddRoleButton, RemoveRoleButton
from modules.buttons.main_button_view import MainButtonView
from modules.buttons.other_buttons.back import BackButton


class RoleManagerView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    def prepare(self, guild_id: int, user_id: int):
        self.add_item(AddRoleButton())
        self.add_item(RemoveRoleButton())

        self.add_item(BackButton(back_view=lambda: MainButtonView().prepare(
            guild_id=guild_id,
            user_id=user_id
        )))

        return self
