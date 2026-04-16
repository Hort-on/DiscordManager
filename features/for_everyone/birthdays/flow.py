from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from features.for_everyone.birthdays.modal import (
    AddAdminBirthdayModal,
    AddBirthdayModal,
    DeleteAdminBirthdayModal,
)
from general_services.other_services.get_member_by_name import get_member_by_name
from general_services.translator.translator import Translator
from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_everyone.birthdays.service import BirthdayService


class BirthdayFlow:
    def __init__(
        self, navigator: Navigator, service: BirthdayService, translator: Translator
    ):
        self.navigator = navigator
        self.service = service
        self.translator = translator

    async def for_add_button(self, interaction: discord.Interaction):
        guild = interaction.guild
        assert guild is not None

        await interaction.response.send_modal(
            AddBirthdayModal(flow=self, translator=self.translator, guild_id=guild.id)
        )

    async def for_delete_button(self, interaction: discord.Interaction):
        guild = interaction.guild
        assert guild is not None

        result = await self.service.delete_birthday(
            user_id=interaction.user.id,
            guild_id=guild.id,
            author_id=interaction.user.id,
        )

        if not result.value:
            embed = ErrorEmbed(description=result.message)
        else:
            embed = SuccessEmbed(description=result.message)

        await interaction.response.edit_message(embed=embed)

    async def save_birthday(
        self, interaction: discord.Interaction, user_birthday: str, user_id: int = None
    ) -> None:
        guild = interaction.guild
        assert guild is not None

        result = await self.service.save_birthday(
            user_id=user_id if user_id is not None else interaction.user.id,
            guild_id=guild.id,
            author_id=interaction.user.id,
            user_birthday=user_birthday,
        )

        if not result.value:
            embed = ErrorEmbed(description=result.message)
        else:
            embed = SuccessEmbed(description=result.message)

        await interaction.followup.send(embed=embed, ephemeral=True)

    async def add_for_admin(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        assert guild is not None

        await interaction.response.send_modal(
            AddAdminBirthdayModal(
                flow=self, translator=self.translator, guild_id=guild.id
            )
        )

    async def delete_for_admin(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        assert guild is not None

        await interaction.response.send_modal(
            DeleteAdminBirthdayModal(
                flow=self, translator=self.translator, guild_id=guild.id
            )
        )

    async def admin_for_add(
        self, interaction: discord.Interaction, user_name: str, user_birthday: str
    ) -> None:
        guild = interaction.guild
        assert guild is not None

        member = get_member_by_name(guild=guild, username=user_name)
        if not member:
            message = self.translator.t(
                guild_id=guild.id, section="SYSTEM_GENERAL", key="error_msg"
            )
            error_embed = ErrorEmbed(description=message)
            await interaction.followup.send(embed=error_embed)
            return

        await self.save_birthday(
            interaction=interaction, user_birthday=user_birthday, user_id=member.id
        )

    async def admin_for_delete(
        self, interaction: discord.Interaction, user_name: str
    ) -> None:
        guild = interaction.guild
        assert guild is not None

        member = get_member_by_name(guild=guild, username=user_name)
        if not member:
            message = self.translator.t(
                guild_id=guild.id, section="SYSTEM_GENERAL", key="error_msg"
            )
            error_embed = ErrorEmbed(description=message)
            await interaction.followup.send(embed=error_embed)
            return

        await self.delete_birthday(interaction=interaction, user_id=member.id)

    async def delete_birthday(
        self, interaction: discord.Interaction, user_id: int
    ) -> None:
        guild = interaction.guild
        assert guild is not None

        result = await self.service.delete_birthday(
            user_id=user_id, guild_id=guild.id, author_id=interaction.user.id
        )

        if not result.value:
            embed = ErrorEmbed(description=result.message)
        else:
            embed = SuccessEmbed(description=result.message)

        await interaction.response.edit_message(embed=embed)
