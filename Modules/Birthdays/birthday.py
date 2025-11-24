import discord
from datetime import datetime
from config import bot
from Modules.Logging.logging import Logger
from db.setup import DB


class Birthday:
    def __init__(self, bot=bot, logger=None, db=None):
        self.bot = bot
        self.logger = logger or Logger()
        self.db = db or DB()

    async def add_new_birthday(self, user_id: int, guild_id: int, user_birthday: str) -> str:
        try:
            datetime.strptime(user_birthday, '%d.%m')
            user = await self.bot.fetch_user(user_id)

            if not user:
                return f"```Could not find the user with ID {user_id}.```"

            with self.db.connect('birthdays') as cursor:
                cursor.execute(
                    "SELECT * FROM Birthdays WHERE user_id = ? AND guild_id = ?",
                    (user_id, guild_id)
                )

                if cursor.fetchone():
                    return f"```The user {user.name} already has a birthday record in the database.```"

                cursor.execute(
                    "INSERT INTO Birthdays (guild_id, user_id, birthday, last_congrats) VALUES (?, ?, ?, ?)",
                    (guild_id, user_id, user_birthday, None)
                )

            return f"```The birthday for {user.display_name} has been successfully added as {user_birthday}.```"

        except ValueError:
            return "```Invalid date format. Please use DD.MM format.```"
        except discord.errors.NotFound:
            return "```The user with ID not found, please check the correctness of the ID.```"
        except Exception as e:
            return f"```Database error: {e}```"

    def delete_birthday(self, user_id: int, guild_id: int) -> str:
        with self.db.connect('birthdays') as cursor:
            cursor.execute(
                "SELECT * FROM Birthdays WHERE user_id = ? AND guild_id = ?",
                (user_id, guild_id)
            )

            if cursor.fetchone():
                cursor.execute(
                    "DELETE FROM Birthdays WHERE user_id = ? AND guild_id = ?",
                    (user_id, guild_id)
                )
                return f"```The user with the ID {user_id} successfully deleted from the DB.```"
            else:
                return f"```The user with the ID {user_id} not found in the DB.```"

    async def check_birthday(self, guild_id: int):
        reset_message = self.reset_last_congrats()
        if reset_message:
            print(reset_message)

        settings = await self.db.get_data(guild_id, "settings", "birthday", "congrats_channel_id")

        if not settings or not settings["birthday"] or not settings["congrats_channel_id"]:
            print(f"Birthday feature is disabled or channel not configured for guild {guild_id}")
            return

        today_birthdays = self.get_today_birthdays(guild_id)
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
                self.update_last_congrats(user_id, guild_id)
                await channel.send(
                    f"Today we celebrate a birthday! 🎉🎂 {member.mention}"
                )
            else:
                with self.db.connect('birthdays') as cursor:
                    cursor.execute(
                        "DELETE FROM Birthdays WHERE user_id = ? AND guild_id = ?",
                        (user_id, guild_id)
                    )
                await self.logger.info(
                    f'The user with the ID: {user_id} has been deleted from the DB.\n'
                    f'The reason is: the user was not found on the server.'
                )

    def get_today_birthdays(self, guild_id: int):
        today = datetime.now().strftime('%d.%m')
        with self.db.connect('birthdays') as cursor:
            cursor.execute("""
                SELECT user_id
                FROM Birthdays
                WHERE guild_id = ?
                  AND birthday = ?
                  AND (last_congrats IS NULL OR last_congrats != ?)
            """, (guild_id, today, today))
            return cursor.fetchall()

    def reset_last_congrats(self):
        today = datetime.now()
        if today.month == 1 and today.day == 1:
            with self.db.connect('birthdays') as cursor:
                cursor.execute("UPDATE Birthdays SET last_congrats = NULL")
            return "The column 'last_congrats' has been reset for all the users in the DB."
        return None

    def update_last_congrats(self, user_id: int, guild_id: int):
        today = datetime.now().strftime('%d.%m')
        with self.db.connect("birthdays") as cursor:
            cursor.execute(
                "UPDATE Birthdays SET last_congrats = ? WHERE user_id = ? AND guild_id = ?",
                (today, user_id, guild_id)
            )