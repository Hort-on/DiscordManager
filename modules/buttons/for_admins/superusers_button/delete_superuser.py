import discord

from database.settings_storage.settings import SettingsStorage

from services.buttons.for_admins.superusers.delete_superuser_service import DeleteSuperuserService
from services.buttons.protection.admin_buttons_protection import FirewallButton
from services.factories.db_factory.db_scenario_factory import DBFactory


class DeleteSuperusersButton(FirewallButton):
    scope = 'admin'

    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBFactory
    ):
        super().__init__(
            label='Delete superusers',
            style=discord.ButtonStyle.green,
        )
        self.service = DeleteSuperuserService(settings=settings, db_factory=db_factory)

    async def on_click(self, interaction: discord.Interaction):
        await self.service.prepare_users(interaction=interaction)
