import discord

from modules.buttons.buttons_for_admins.edit_settings_button.service.setting_selection import SettingSelectorView
from modules.buttons.buttons_for_admins.edit_settings_button.service.settings_formatter import SettingsFormatter


class EditSettingsButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Edit settings",
            style=discord.ButtonStyle.green
        )
        self.settings_formatter = SettingsFormatter()

    async def callback(self, interaction: discord.Interaction):
        self.view.disable_all_items()
        summary = self.settings_formatter.format_settings(interaction)

        view = SettingSelectorView()

        await interaction.response.send_message(
            summary,
            view=view,
            ephemeral=True
        )
