import discord

from modules.birthdays.birthday_repo import BirthdayRepo


class DeleteBirthdayService:
    def __init__(self, birthday: BirthdayRepo):
        self.birthday = birthday

    async def delete_process(
            self,
            interaction: discord.Interaction,
            username: str,
    ) -> None:

        member = (
            discord.utils.get(interaction.guild.members, name=username)
            or discord.utils.get(interaction.guild.members, display_name=username)
        )

        if member is None:
            await interaction.edit_original_response(
                content='❌ User not found. Check username.',
            )
            return

        b_day = self.birthday
        response = await b_day.delete_birthday(
            interaction,
            member.id,
            interaction.guild.id
        )

        await interaction.edit_original_response(content=response)
        