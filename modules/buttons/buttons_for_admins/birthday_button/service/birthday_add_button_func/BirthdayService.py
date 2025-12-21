import discord
from modules.birthdays.birthday import Birthday


class AddBirthdayService:

    @staticmethod
    async def process(
        interaction: discord.Interaction,
        username: str,
        birthday: str
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

        if not AddBirthdayService._is_valid_date(birthday):
            await interaction.response.send_message(
                "❌ Invalid date format. Use DD.MM",
                ephemeral=True
            )
            return

        b_day = Birthday()
        response = await b_day.add_new_birthday(
            member.id,
            interaction.guild.id,
            birthday
        )

        await interaction.response.send_message(
            response,
            ephemeral=True
        )

    @staticmethod
    def _is_valid_date(value: str) -> bool:
        try:
            day, month = map(int, value.split("."))
            return 1 <= day <= 31 and 1 <= month <= 12
        except ValueError:
            return False
