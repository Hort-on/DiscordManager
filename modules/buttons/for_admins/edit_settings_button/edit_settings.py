import discord

from database.settings_storage.settings import SettingsStorage

from services.buttons.for_admins.edit_settings_service.settings_formater import SettingsFormatter
from services.buttons.for_admins.edit_settings_service.settings_selection import SettingSelectorView
from services.buttons.protection.admin_buttons_protection import FirewallButton
from services.factories.db_factory.db_scenario_factory import DBScenarioFactory


class EditSettingsButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBScenarioFactory
    ):
        super().__init__(
            label='Edit settings',
            style=discord.ButtonStyle.green
        )

        self.db_factory = db_factory

        self.settings_formatter = SettingsFormatter(settings)

    async def on_click(self, interaction: discord.Interaction) -> None:
        summary = await self.settings_formatter.format_settings(interaction)

        view = SettingSelectorView(
            guild_id=interaction.guild_id,
            user_id=interaction.user.id,
            db_factory=self.db_factory
        )

        await interaction.edit_original_response(
            content=summary,
            view=view,
        )
