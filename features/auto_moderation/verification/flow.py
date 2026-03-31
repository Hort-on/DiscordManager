from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings_manager import StorageTarget

from features.auto_moderation.verification.modals import AntiBotModal

from ui.embed_constructor.embed_constructor import InfoEmbed, ErrorEmbed, SuccessEmbed

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.settings_storage.settings import SettingsStorage
    from features.auto_moderation.verification.service import VerificationService
    from general_services.translator.translator import Translator


@dataclass
class AssignVerificationRoleResult:
    value: bool
    message: str


class VerificationFlow:
    def __init__(
            self,
            bot: Bot,
            settings: SettingsStorage,
            service: VerificationService,
            translator: Translator
    ):
        self.bot = bot
        self.settings = settings
        self.service = service
        self.translator = translator

        self.users_count: dict[tuple[int, int], int] = {}

    async def agreement_start(self, interaction: discord.Interaction):
        guild = interaction.guild
        assert guild is not None

        anti_bot = self.settings.dict_storage.get_value(
            key='anti_bot',
            target=StorageTarget.SETTINGS,
            guild_id=guild.id
        )

        if bool(anti_bot):
            await interaction.response.send_modal(
                AntiBotModal(
                    flow=self,
                    translator=self.translator,
                    guild_id=guild.id
                )
            )
            return

        result = await self._assign_role(
            guild=guild,
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

        guild = interaction.guild
        assert guild is not None

        result_word = await self._check_the_word(
            guild_id=guild.id,
            member=interaction.user,
            word=word
        )

        if not result_word:
            fail_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=guild.id,
                    section='VERIFICATION',
                    key='wrong_word'
                )
            )
            await interaction.followup.send(embed=fail_embed)

            return

        result = await self._assign_role(
            guild=guild,
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

    async def disagreement_start(self, interaction: discord.Interaction):
        guild = interaction.guild
        assert guild is not None

        info_embed = InfoEmbed(
            description=self.translator.t(
                guild_id=guild.id,
                section='VERIFICATION',
                key='declined'
            )
        )
        await interaction.response.send_message(
            embed=info_embed,
            ephemeral=True
        )

    async def _check_the_word(
            self,
            guild_id: int,
            member: discord.User | discord.Member,
            word: str
    ) -> bool:

        if word.lower() != 'hello':
            key = (member.id, guild_id)

            count = self.users_count.get(key, 0) + 1
            self.users_count[key] = count

            if count >= 2:
                try:
                    msg = self.translator.t(
                        guild_id=guild_id,
                        section='VERIFICATION',
                        key='not_passed'
                    )
                    await member.kick(reason=msg)
                except discord.Forbidden:
                    pass
                finally:
                    self.users_count.pop(key, None)

            return False

        return True

    async def _assign_role(
            self,
            guild: discord.Guild,
            member: discord.User | discord.Member
    ) -> AssignVerificationRoleResult:

        verification_role = self.settings.dict_storage.get_value(
            key='verification_role_id',
            target=StorageTarget.SETTINGS,
            guild_id=guild.id
        )

        if not verification_role:
            message = self.translator.t(
                guild_id=guild.id,
                section='VERIFICATION',
                key='role_not_assigned'
            )

            return AssignVerificationRoleResult(
                value=False,
                message=message
            )

        role = guild.get_role(verification_role)
        if not role:
            message = self.translator.t(
                guild_id=guild.id,
                section='VERIFICATION',
                key='role_not_found'
            )
            return AssignVerificationRoleResult(
                value=False,
                message=message
            )

        await member.add_roles(role)

        self.users_count.pop((member.id, guild.id), None)

        message = self.translator.t(
            guild_id=guild.id,
            section='VERIFICATION',
            key='welcome_msg'
        )
        return AssignVerificationRoleResult(
            value=True,
            message=message
        )
