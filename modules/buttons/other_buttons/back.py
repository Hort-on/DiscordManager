import discord

from modules.buttons.services.protection.admin_buttons_protection import FirewallButton


class BackButton(FirewallButton):
    scope = 'admin'

    def __init__(self, back_view):
        super().__init__(
            label='↩️ Back',
            style=discord.ButtonStyle.secondary
        )
        self.back_view = back_view

    async def on_click(self, interaction: discord.Interaction) -> None:
        await interaction.edit_original_response(
            view=self.back_view()
        )
