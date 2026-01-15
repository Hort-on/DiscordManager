import discord

from modules.birthdays.birthday_repo import BirthdayManager
from services.other_services.get_member_by_name import get_member_by_name


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
            await interaction.edit_original_response(
                content='❌ User not found. Check username.',
            )
            return

        b_day = self.birthday_manager
        response = await b_day.delete_birthday(
            interaction=interaction,
            user_id=member.id,
            guild_id=interaction.guild.id
        )

        await interaction.edit_original_response(content=response)
        