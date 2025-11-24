import discord

from Modules.Management.buttons.edit_settings_view.setting_selection import SettingSelectorView
from Modules.Management.buttons.edit_settings_view.settings_formatter import SettingsFormatter


class EditSettingsButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Edit settings",
            style=discord.ButtonStyle.green
        )
        self.settings_formatter = SettingsFormatter()

    async def callback(self, interaction: discord.Interaction):
        summary = self.settings_formatter.format_settings(interaction)

        view = SettingSelectorView()

        await interaction.response.send_message(
            summary,
            view=view,
            ephemeral=True
        )
