from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings_manager import StorageTarget

from features.auto_moderation.verification.modals import AntiBotModal

from ui.embed_constructor.embed_constructor import InfoEmbed, ErrorEmbed, SuccessEmbed

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.settings_storage.settings import SettingsStorage
    from features.auto_moderation.verification.service import VerificationService


class VerificationFlow:
    def __init__(
            self,
            bot: Bot,
            settings: SettingsStorage,
            service: VerificationService
    ):
        self.bot = bot
        self.settings = settings
        self.service = service

    async def agreement_start(self, interaction: discord.Interaction):
        anti_bot = self.settings.dict_storage.get_value(
            'anti_bot',
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id
        )

        if bool(anti_bot):
            await interaction.response.send_modal(AntiBotModal(
                flow=self
            ))
            return

        result = await self.service.assign_role(
            guild=interaction.guild,
            member=interaction.user
        )

        if not result.value:
            error_embed = ErrorEmbed(
                description=result.message
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return

        success_embed = SuccessEmbed(
            description=result.message
        )

        await interaction.response.send_message(embed=success_embed, ephemeral=True)

    async def word_verification(self, interaction: discord.Interaction, word: str) -> None:
        await interaction.response.defer(ephemeral=True)

        result_word = await self.service.check_the_word(
            guild_id=interaction.guild_id,
            member=interaction.user,
            word=word
        )

        if not result_word:
            fail_embed = ErrorEmbed(
                description='You wrote the word incorrectly.'
                            ' You have one more attempt.'
                            ' If you fail, you will be kicked off the server'
            )
            await interaction.followup.send(embed=fail_embed)

            return

        result = await self.service.assign_role(
            guild=interaction.guild,
            member=interaction.user
        )

        if not result.value:
            embed = ErrorEmbed(
                description=result.message
            )
        else:
            embed = SuccessEmbed(
                description=result.message
            )

        await interaction.followup.send(embed=embed)

    @staticmethod
    async def disagreement_start(interaction: discord.Interaction):
        info_embed = InfoEmbed(
            description='You have declined the rules, you will not be given an access to this server,'
                        ' until you agree with the rules.'
        )
        await interaction.response.send_message(
            embed=info_embed,
            ephemeral=True
        )
