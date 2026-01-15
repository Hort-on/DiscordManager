import discord

from modules.buttons.for_admins.delete_message.any_msg import DeleteAnyMessageButton
from modules.buttons.for_admins.delete_message.msg_from_users import DeleteUserMessageButton
from modules.buttons.others.back import BackButton
from modules.buttons.views.for_admins.admin_menu import AdminMenuView


class DeleteMsgMenuView(discord.ui.View):
    def __init__(self, guild_id: int, user_id: int):
        super().__init__(timeout=60)

        self.add_item(DeleteAnyMessageButton())
        self.add_item(DeleteUserMessageButton())
        self.add_item(BackButton(lambda: AdminMenuView(guild_id=guild_id, user_id=user_id)))
