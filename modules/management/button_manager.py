import discord

from discord.ui import View

from database.settings_storage.settings_manager import StorageTarget

from dependency_injector.wiring import inject, Provide

from core.bot_container import BotContainer

from modules.buttons.for_users.randomizer.start import RandomStartButton
from modules.buttons.others.admin_menu import AdminMenuButton


class ButtonManager(View):
    @inject
    def __init__(
            self,
            interaction: discord.Interaction,
            settings=Provide[BotContainer.settings],
    ):

        super().__init__(timeout=60)
        self.interaction = interaction
        self.settings = settings

        self._add_buttons()

    def _add_buttons(self):
        superusers = self.settings.set_storage.get_for_set(
            target=StorageTarget.SUPERUSERS,
            guild_id=self.interaction.guild_id
        )

        self.add_item(RandomStartButton())

        if self.interaction.user.id in superusers:
            self._add_admin_panel()

    def _add_admin_panel(self):
        self.add_item(AdminMenuButton())
