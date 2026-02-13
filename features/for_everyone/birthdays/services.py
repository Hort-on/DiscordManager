from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from features.birthdays.birthday_manager import BirthdayManager

import discord

from general_services.other_services.get_member_by_name import get_member_by_name


class AddBirthdayService:
    def __init__(self, birthday_manager: BirthdayManager):
        self.birthday_manager = birthday_manager

    async def add_process(
            self,
            interaction: discord.Interaction,
            username: str,
            birthday: str
    ) -> None:

        member = get_member_by_name(
            interaction=interaction,
            username=username
        )

        if member is None:
            await interaction.response.edit_message(
                content='```❌ User not found. Please check username.```',
            )
            return

        if not AddBirthdayService._is_valid_date(birthday):
            await interaction.response.edit_message(
                content='```❌ Invalid date format. Use DD.MM```',
            )
            return

        b_day = self.birthday_manager
        await b_day.add_new_birthday(
            interaction=interaction,
            user_id=member.id,
            guild_id=interaction.guild.id,
            user_birthday=birthday
        )

    @staticmethod
    def _is_valid_date(value: str) -> bool:
        try:
            day, month = map(int, value.split("."))
            return 1 <= day <= 31 and 1 <= month <= 12
        except ValueError:
            return False


class DeleteBirthdayService:
    def __init__(self, birthday_manager: BirthdayManager):
        self.birthday_manager = birthday_manager

    async def delete_process(
            self,
            interaction: discord.Interaction,
            username: str,
    ) -> None:
        member = get_member_by_name(
            interaction=interaction,
            username=username
        )

        if member is None:
            await interaction.response.edit_message(
                content='❌ User not found. Check username.',
            )
            return

        b_day = self.birthday_manager
        response = await b_day.delete_birthday(
            interaction=interaction,
            user_id=member.id,
            guild_id=interaction.guild.id
        )

        await interaction.response.edit_message(content=response)
