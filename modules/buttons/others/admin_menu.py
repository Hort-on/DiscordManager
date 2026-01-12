import discord

from modules.buttons.views.for_admins.admin_menu import AdminMenuView


class AdminMenuButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Admin menu',
            style=discord.ButtonStyle.secondary
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.disable_all_items()
        view = AdminMenuView(interaction.guild_id)

        await interaction.edit_original_response(
            view=view
        )
