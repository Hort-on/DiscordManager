from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings_manager import StorageTarget

from features.auto_moderation.verification.modals import AntiBotModal

from ui.embed_constructor.embed_constructor import InfoEmbed, ErrorEmbed

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage
    from ui.yes_no_service.yes_no_factory import YesNoViewFactory
    from features.auto_moderation.verification.service import VerificationService


class VerificationFlow:
    def __init__(
            self,
            settings: SettingsStorage,
            yes_no_factory: YesNoViewFactory,
            service: VerificationService
    ):
        self.settings = settings
        self.yes_no = yes_no_factory
        self.service = service

    async def agree_start(self, interaction: discord.Interaction):
        anti_bot = self.settings.dict_storage.for_dict_get(
            'anti_bot',
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id
        )

        if anti_bot:
            await interaction.response.send_modal(AntiBotModal(
                flow=self
            ))
            return

        await self.service.assign_role(interaction=interaction)

    async def word_verification(self, interaction: discord.Interaction, word: str):
        await interaction.response.defer(ephemeral=True)

        result = self.service.check_the_word()

        fail_embed = ErrorEmbed(
            description='You wrote the word incorrectly.'
                        ' You have one more attempt.'
                        ' If you fail, you will be kicked off the server'
        )
        await interaction.response.send_message(
            embed=fail_embed,
            ephemeral=True
        )

        return

        await self.assign_role(interaction=interaction)

    @staticmethod
    async def disagree_start(interaction: discord.Interaction):
        info_embed = InfoEmbed(
            description='You have declined the rules, you will not be given an access to this server,'
                        ' until you agree with the rules.'
        )
        await interaction.response.send_message(
            embed=info_embed,
            ephemeral=True
        )
