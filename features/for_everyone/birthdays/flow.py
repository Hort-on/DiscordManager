from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.for_everyone.birthdays.modals import AddBirthdayModal

from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_everyone.birthdays.service import BirthdayService


class BirthdayFlow:
    def __init__(self, navigator: Navigator, service: BirthdayService):
        self.navigator = navigator
        self.service = service

    async def for_add_button(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AddBirthdayModal(flow=self))

    async def for_delete_button(self, interaction: discord.Interaction):
        result = await self.service.delete_birthday(
            user_id=interaction.user.id,
            guild_id=interaction.guild_id
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

        result = await self.service.save_birthday(
            user_id=interaction.user.id,
            guild_id=interaction.guild_id,
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
