import discord

from modules.buttons.for_admins.delete_message.menu_view import DeleteMsgMenuView
from modules.buttons.services.protection.admin_buttons_protection import FirewallButton


class DeleteMsgMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Delete message',
            style=discord.ButtonStyle.blurple
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        view = DeleteMsgMenuView().prepare(
            guild_id=interaction.guild_id,
            user_id=interaction.user.id
        )
        await interaction.edit_original_response(view=view)
