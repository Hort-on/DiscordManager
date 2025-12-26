import discord

from modules.birthdays.birthday_repo import Birthday


class DeleteBirthdayService:

    @staticmethod
    async def process(
            interaction: discord.Interaction,
            username: str,
    ) -> None:

        member = (
            discord.utils.get(interaction.guild.members, name=username)
            or discord.utils.get(interaction.guild.members, display_name=username)
        )

        if member is None:
            await interaction.response.send_message(
                "❌ User not found. Check username.",
                ephemeral=True
            )
            return

        b_day = Birthday()
        response = await b_day.delete_birthday(
            member.id,
            interaction.guild.id
        )

        await interaction.response.send_message(
            response,
            ephemeral=True
        )
        