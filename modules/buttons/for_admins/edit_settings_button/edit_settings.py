import discord

from modules.buttons.for_admins.edit_settings_button.services import SettingsFormatter, SettingSelectorView
from modules.buttons.services.protection.admin_buttons_protection import FirewallButton


class EditSettingsButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Edit settings',
            style=discord.ButtonStyle.green
        )
        self.settings_format = SettingsFormatter()

    async def on_click(self, interaction: discord.Interaction) -> None:
        summary = await self.settings_format.format_settings(interaction)

        view = SettingSelectorView().prepare(
            guild_id=interaction.guild_id,
            user_id=interaction.user.id
        )

        await interaction.edit_original_response(
            content=summary,
            view=view
        )
