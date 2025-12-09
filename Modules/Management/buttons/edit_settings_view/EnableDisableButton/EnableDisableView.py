import discord
from discord.ui import View
from Modules.Management.buttons.edit_settings_view.setting_selection import SettingSelectorView
from db.data_base_setup import DB
from db.messages import EDIT_CONFIG_MESSAGES as ECM


class EnableDisableView(View):
    def __init__(self, config_key: str):
        super().__init__(timeout=60)
        self.db = DB()
        self.config_key = config_key

    async def _apply_change(self, interaction: discord.Interaction, value: bool) -> None:
        for item in self.children:
            item.disabled = True

        await interaction.response.defer()

        try:
            await self.db.write_data(
                interaction.guild.id,
                "settings",
                {self.config_key: value}
            )

            await interaction.message.edit(
                content=ECM.get("success_editing_msg"),
                view=SettingSelectorView()
            )

        except Exception as e:
            print("[DB ERROR]", e)
            await interaction.message.edit(
                content=ECM.get("failed_editing_msg"),
                view=SettingSelectorView()
            )

    @discord.ui.button(label="Enable", style=discord.ButtonStyle.green)
    async def enable_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._apply_change(interaction, True)

    @discord.ui.button(label="Disable", style=discord.ButtonStyle.red)
    async def disable_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._apply_change(interaction, False)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.gray)
    async def back_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            content=ECM.get("config_editing_msg"),
            view=SettingSelectorView()
        )
