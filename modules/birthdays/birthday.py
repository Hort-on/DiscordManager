import discord
from datetime import datetime
from modules.Logging.logging import Logger
from database.birthday_db_repo import BirthdayDbActions
from bot import bot


class Birthday:
    def __init__(self):
        self.bot = bot
        self.logger = Logger()
        self.repo = BirthdayDbActions()

    async def add_new_birthday(self, user_id: int, guild_id: int, user_birthday: str) -> str:
        try:
            datetime.strptime(user_birthday, '%d.%m')
            user = await self.bot.fetch_user(user_id)

            if not user:
                return f"```Could not find the user with ID {user_id}.```"

            if not await self.repo.birthday_exists(user_id, guild_id):
                await self.repo.insert_birthday(guild_id, user_id, user_birthday)

            return f"```The birthday for {user.display_name} has been successfully added as {user_birthday}.```"

        except ValueError:
            return "```Invalid date format. Please use DD.MM format.```"
        except discord.errors.NotFound:
            return "```The user with ID not found, please check the correctness of the ID.```"
        except Exception as e:
            return f"```Database error: {e}```"

    async def delete_birthday(self, user_id: int, guild_id: int) -> str:
        if await self.repo.birthday_exists(user_id, guild_id):
            await self.repo.delete_birthday(user_id, guild_id)
            return f"```The user with the ID {user_id} successfully deleted from the DB.```"
        else:
            return f"```The user with the ID {user_id} not found in the DB.```"

    async def check_birthday(self, guild_id: int):
        #TODO: Розбити функцію на підблоки
        today = datetime.now()
        if today.month == 1 and today.day == 1:
            await self.repo.reset_all_congrats()
            print("The column 'last_congrats' has been reset for all the users in the DB.")

        settings = await self.repo.db.get_data(guild_id, "settings", "birthday", "congrats_channel_id")

        if not settings or not settings["birthday"] or not settings["congrats_channel_id"]:
            print(f"Birthday feature is disabled or channel not configured for guild {guild_id}")
            return

        today_str = today.strftime('%d.%m')
        today_birthdays = await self.repo.get_today_birthdays(guild_id, today_str)
        guild = self.bot.get_guild(guild_id)

        if not guild or not today_birthdays:
            return

        channel = self.bot.get_channel(settings["congrats_channel_id"])
        if not channel:
            print(f"Channel {settings['congrats_channel_id']} not found")
            return

        for user_id_tuple in today_birthdays:
            user_id = user_id_tuple[0]
            member = guild.get_member(user_id)

            if member:
                await self.repo.update_last_congrats(user_id, guild_id, today_str)
                await channel.send(
                    f"Today we celebrate a birthday! 🎉🎂 {member.mention}"
                )
            else:
                await self.repo.delete_birthday(user_id, guild_id)
                await self.logger.info(
                    f'The user with the ID: {user_id} has been deleted from the DB.\n'
                    f'The reason is: the user was not found on the server.'
                )
