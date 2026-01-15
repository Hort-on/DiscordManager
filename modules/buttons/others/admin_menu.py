import discord

from modules.buttons.views.for_admins.admin_menu import AdminMenuView
from services.buttons.protection.admin_buttons_protection import FirewallButton


class AdminMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Admin menu',
            style=discord.ButtonStyle.secondary
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.disable_all_items()
        view = AdminMenuView(guild_id=interaction.guild_id, user_id=interaction.user.id)

        await interaction.edit_original_response(
            view=view
        )
