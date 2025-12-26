import discord

from datetime import datetime

from database.db_factory.db_scenario_factory import DBScenarioFactory
from bot import bot


class Birthday:
    def __init__(self):
        self.bot = bot
        self.factory = DBScenarioFactory()

    async def add_new_birthday(
            self,
            interaction: discord.Interaction,
            user_id: int,
            guild_id: int,
            user_birthday: str
    ) -> None:

        try:
            datetime.strptime(user_birthday, '%d.%m')
        except ValueError:
            await interaction.edit_original_response(
                content="```Invalid date format. Use DD.MM```"
            )
            return

        member = interaction.guild.get_member(user_id)
        if not member:
            await interaction.edit_original_response(
                content="```User not found in this server.```"
            )
            return

        exists_scenario = self.factory.for_exists_birthday_check(guild_id, user_id)
        if await exists_scenario.proceed():
            await interaction.edit_original_response(
                content=f"```{member.display_name} already has a birthday set.```"
            )
            return

        add_scenario = self.factory.for_add_birthday(guild_id, user_id, user_birthday)
        if await add_scenario.proceed():
            await interaction.edit_original_response(
                content=f"```The birthday for {member.display_name} has been successfully added as {user_birthday}.```"
            )
            return

        await interaction.edit_original_response(
            content="```Something went wrong, please try again.```"
        )

    async def delete_birthday(
            self,
            interaction : discord.Interaction,
            user_id: int,
            guild_id: int
    ) -> None:

        exists_scenario = self.factory.for_exists_birthday_check(guild_id, user_id)
        if not await exists_scenario.proceed():
            await interaction.edit_original_response(
                content=f"```The user with the ID {user_id} not found in the DB.```"
            )
            return

        delete_scenario = self.factory.for_delete_birthday(guild_id, user_id)
        if await delete_scenario.proceed():
            await interaction.edit_original_response(
                content=f"```The user with the ID {user_id} successfully deleted from the DB.```"
            )
            return

        await interaction.edit_original_response(
            content="```Something went wrong, please try again.```"
        )

    async def check_daily_birthday(self, guild_id: int) -> None:
        today = datetime.now()
        today_str = today.strftime('%d.%m')

        if today.month == 1 and today.day == 1:
            reset_scenario = self.factory.for_reset_congrats()
            await reset_scenario.proceed()

        today_birthdays_scenario = self.factory.for_get_today_birthday(
            guild_id,
            today_str
        )
        birthdays = await today_birthdays_scenario.proceed()

        if not birthdays:
            return

        await self.prepare_data(guild_id, today_str, birthdays)

    async def prepare_data(self, guild_id: int, today_str, birthdays) -> None:
        settings_scenario = self.factory.for_get_data(
            guild_id,
            "settings",
            "congrats_channel_id"
        )
        settings = await settings_scenario.proceed()

        if not settings:
            return

        channel = self.bot.get_channel(settings.get("congrats_channel_id"))
        if not channel:
            return

        guild = self.bot.get_guild(guild_id)
        if not guild:
            return

        await self.send_congrats(guild, channel, birthdays, today_str)

    async def send_congrats(self, guild, channel, birthdays, today_str) -> None:
        for user_id_tuple in birthdays:
            user_id = user_id_tuple[0]
            member = guild.get_member(user_id)

            if not member:
                delete_scenario = self.factory.for_delete_birthday(guild.id, user_id)
                await delete_scenario.proceed()
                continue

            await channel.send(
                f"Today we celebrate a birthday! 🎉🎂 {member.mention}"
            )

            await self.update_congrats(guild.id, user_id, today_str)

    async def update_congrats(self, guild_id: int, user_id, today_str) -> None:
        update_scenario = self.factory.for_update_last_congrats(guild_id, user_id, today_str)
        await update_scenario.proceed()
