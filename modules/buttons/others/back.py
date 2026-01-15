import discord

from services.buttons.protection.admin_buttons_protection import FirewallButton


class BackButton(FirewallButton):
    scope = 'admin'

    def __init__(self, view_factory):
        super().__init__(
            label='↩️ Back',
            style=discord.ButtonStyle.secondary
        )
        self.view_factory = view_factory

    async def on_click(self, interaction: discord.Interaction) -> None:
        if self.view:
            self.view.disable_all_items()
            await interaction.edit_original_response(view=self.view)

        await interaction.edit_original_response(
            view=self.view_factory()
        )
