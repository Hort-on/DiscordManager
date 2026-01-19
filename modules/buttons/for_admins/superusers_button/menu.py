import discord

from modules.buttons.for_admins.superusers_button.menu_view import SuperusersMenuView
from modules.buttons.services.protection.admin_buttons_protection import FirewallButton


class SuperusersMenuButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Superusers management',
            style=discord.ButtonStyle.green
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        view = SuperusersMenuView().prepare(
            guild_id=interaction.guild_id,
            user_id=interaction.user.id
        )
        await interaction.edit_original_response(view=view)
