from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.for_everyone.birthdays.modal import AddBirthdayModal
from general_services.translator.translator import Translator

from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_everyone.birthdays.service import BirthdayService


class BirthdayFlow:
    def __init__(self, navigator: Navigator, service: BirthdayService, translator: Translator):
        self.navigator = navigator
        self.service = service
        self.translator = translator

    async def for_add_button(self, interaction: discord.Interaction):
        guild = interaction.guild
        assert guild is not None

        await interaction.response.send_modal(
            AddBirthdayModal(
                flow=self,
                translator=self.translator,
                guild_id=guild.id
            )
        )

    # TODO: зробити функціонал для додавання з адмінів
    async def for_delete_button(self, interaction: discord.Interaction):
        guild = interaction.guild
        assert guild is not None

        result = await self.service.delete_birthday(
            user_id=interaction.user.id,
            guild_id=guild.id,
            author_id=interaction.user.id
        )

        if not result.value:
            embed = ErrorEmbed(
                description=result.message
            )
        else:
            embed = SuccessEmbed(
                description=result.message
            )

        await interaction.response.edit_message(embed=embed)

    async def add_birthday(self, interaction: discord.Interaction, user_birthday: str) -> None:
        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild
        assert guild is not None

        result = await self.service.save_birthday(
            user_id=interaction.user.id,
            guild_id=guild.id,
            author_id=interaction.user.id,
            user_birthday=user_birthday
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
