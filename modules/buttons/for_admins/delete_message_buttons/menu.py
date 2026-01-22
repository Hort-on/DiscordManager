import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.buttons.for_admins.delete_message_buttons.menu_view import DeleteMsgMenuView


class DeleteMsgMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Delete message',
            style=discord.ButtonStyle.blurple
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        view = DeleteMsgMenuView()
        await interaction.edit_original_response(view=view)
