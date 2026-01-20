import discord

from modules.buttons.for_users.role_manager.menu_view import RoleManagerView
from modules.buttons.services.protection.admin_buttons_protection import FirewallButton


class RoleManagerMenuButton(FirewallButton):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='Role manager',
            style=discord.ButtonStyle.secondary
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        view = RoleManagerView().prepare(
            guild_id=interaction.guild_id,
            user_id=interaction.user.id
        )
        await interaction.edit_original_response(view=view)
