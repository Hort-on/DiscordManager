from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.yes_no_service.yes_no_factory import YesNoViewFactory
    from database.settings_storage.settings import SettingsStorage

import discord

from database.settings_storage.settings_manager import StorageTarget

from features.verification.modals import AntiBotModal
from features.verification.service import AgreeButtonService

from ui.button_protection.admin_buttons_protection import FirewallButton
from ui.embed_constructor.embed_constructor import InfoEmbed


class AgreeButton(FirewallButton):
    scope = 'user'

    def __init__(
            self,
            settings: SettingsStorage,
            yes_no_factory: YesNoViewFactory
    ):
        super().__init__(
            label='Agree',
            style=discord.ButtonStyle.green,
            custom_id='verify_agree'
        )

        self.settings = settings
        self.yes_no_factory = yes_no_factory

    async def on_click(self, interaction: discord.Interaction) -> None:
        anti_bot = self.settings.dict_storage.for_dict_get(
            'anti_bot',
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id
        )

        if anti_bot:
            await interaction.response.send_modal(AntiBotModal())
            return

        service = AgreeButtonService(
            settings=self.settings,
            yes_no_factory=self.yes_no_factory
        )

        await service.assign_role(interaction=interaction)


class DisagreeButton(FirewallButton):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='Disagree',
            style=discord.ButtonStyle.red,
            custom_id='verify_disagree'
        )

    async def on_click(self, interaction: discord.Interaction):
        info_embed = InfoEmbed(
            description='You have declined the rules, you will not be given an access to this server,'
                        ' until you agree with the rules.'
        )
        await interaction.response.send_message(
            embed=info_embed,
            ephemeral=True
        )
