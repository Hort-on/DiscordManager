import discord

from modules.birthdays.birthday_repo import BirthdayRepo


class AddBirthdayService:
    def __init__(self, birthday: BirthdayRepo):
        self.birthday = birthday

    async def add_process(
            self,
            interaction: discord.Interaction,
            username: str,
            birthday: str
    ) -> None:

        member = (
                discord.utils.get(interaction.guild.members, name=username)
                or discord.utils.get(interaction.guild.members, display_name=username)
        )

        if member is None:
            await interaction.edit_original_response(
                content='```❌ User not found. Please check username.```',
            )
            return

        if not AddBirthdayService._is_valid_date(birthday):
            await interaction.edit_original_response(
                content='```❌ Invalid date format. Use DD.MM```',
            )
            return

        b_day = self.birthday
        await b_day.add_new_birthday(
            interaction,
            member.id,
            interaction.guild.id,
            birthday
        )

    @staticmethod
    def _is_valid_date(value: str) -> bool:
        try:
            day, month = map(int, value.split("."))
            return 1 <= day <= 31 and 1 <= month <= 12
        except ValueError:
            return False
