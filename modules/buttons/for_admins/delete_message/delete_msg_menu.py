import discord

from modules.buttons.views.for_admins.delete_msg_menu import DeleteMsgMenuView

from services.buttons.protection.admin_buttons_protection import FirewallButton


class DeleteMsgMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self,
                 guild_id: int,
                 user_id: int
                 ):
        super().__init__(
            label='Delete message',
            style=discord.ButtonStyle.blurple
        )

        self.guild_id = guild_id
        self.user_id = user_id

    async def on_click(self, interaction: discord.Interaction) -> None:
        view = DeleteMsgMenuView(guild_id=self.guild_id, user_id=self.user_id)
        await interaction.edit_original_response(view=view)
