from database.data_base_model import DB


class BirthdayDbActions:
    """Centralized repository for working with birthday databases"""

    def __init__(self):
        self.db = DB()

    async def insert_birthday(self, guild_id: int, user_id: int, birthday: str):
        """Adds a new birthday"""
        async with self.db.connect('birthdays') as cursor:
            await cursor.execute(
                "INSERT INTO birthdays (guild_id, user_id, birthday, last_congrats) VALUES (?, ?, ?, ?)",
                (guild_id, user_id, birthday, None)
            )

    async def delete_birthday(self, user_id: int, guild_id: int):
        """Deletes birthday"""
        async with self.db.connect('birthdays') as cursor:
            await cursor.execute(
                "DELETE FROM birthdays WHERE user_id = ? AND guild_id = ?",
                (user_id, guild_id)
            )

    async def get_birthday(self, user_id: int, guild_id: int):
        """Receives the birthday of a specific user"""
        async with self.db.connect('birthdays') as cursor:
            await cursor.execute(
                "SELECT * FROM birthdays WHERE user_id = ? AND guild_id = ?",
                (user_id, guild_id)
            )
            return await cursor.fetchone()

    async def get_today_birthdays(self, guild_id: int, today: str):
        """Receives all birthdays for today"""
        async with self.db.connect('birthdays') as cursor:
            await cursor.execute("""
                SELECT user_id
                FROM birthdays
                WHERE guild_id = ?
                  AND birthday = ?
                  AND (last_congrats IS NULL OR last_congrats != ?)
            """, (guild_id, today, today))
            return await cursor.fetchall()

    async def update_last_congrats(self, user_id: int, guild_id: int, date: str):
        """Updates the date of the last congrats"""
        async with self.db.connect("birthdays") as cursor:
            await cursor.execute(
                "UPDATE birthdays SET last_congrats = ? WHERE user_id = ? AND guild_id = ?",
                (date, user_id, guild_id)
            )

    async def reset_all_congrats(self):
        """Resets all last congrats (on a new year)"""
        async with self.db.connect('birthdays') as cursor:
            await cursor.execute("UPDATE birthdays SET last_congrats = NULL")

    async def birthday_exists(self, user_id: int, guild_id: int) -> bool:
        """Checks whether the user with the birthday already exists in the database for this guild"""
        result = await self.get_birthday(user_id, guild_id)
        return result is not None
