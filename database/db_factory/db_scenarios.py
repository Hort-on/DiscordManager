from database.data_base_model import DB


class BaseScenario:
    table_map = {
        'settings': "GuildSettings",
        'super_users': "SuperUsers",
        'channels': "SelectedChannels",
        'birthdays': "Birthdays"
    }

    def _get_table(self, table_name: str) -> str:
        table = self.table_map.get(table_name)
        if not table:
            raise ValueError(f"Unknown table name: {table_name}")
        return table


    async def proceed(self, **kwargs):
        raise NotImplementedError


class GetDataScenario(BaseScenario):
    def __init__(self):
        super().__init__()
        self.db = DB()

    async def proceed(self, guild_id, table_name,  *columns) -> dict | None:
        table = self._get_table(table_name)
        columns_sql = ", ".join(columns)
        query = f"SELECT {columns_sql} FROM {table} WHERE guild_id = ?"

        async with self.db.connect() as db:
            async with db.execute(query, (guild_id,)) as cursor:
                col_names = [desc[0] for desc in cursor.description]

                row = await cursor.fetchone()
                return dict(zip(col_names, row)) if row else None


class WriteDataScenario(BaseScenario):
    def __init__(self):
        super().__init__()
        self.db = DB()

    async def proceed(self, guild_id: int, table_name: str, data: dict) -> bool:
        table = self._get_table(table_name)

        async with self.db._write_lock:
            async with self.db.connect() as db:
                columns = ", ".join(["guild_id", *data.keys()])
                placeholders = ", ".join(["?"] * (len(data) + 1))
                update_clause = ", ".join(f"{k}=excluded.{k}" for k in data.keys())
                query = f"""INSERT INTO {table} ({columns}) VALUE ({placeholders})
                        ON CONFLICT(guild_id) DO UPDATE SET {update_clause}"""

                await db.execute(query, (guild_id, *data.values()))
                await db.commit()
                return True

class FetchAllDataScenario(BaseScenario):
    def __init__(self):
        super().__init__()
        self.db = DB()

    async def proceed(self, guild_id: int, table_name: str) -> list[dict]:
        table = self._get_table(table_name)
        query = f"SELECT * FROM {table} WHERE guild_id = ?"

        async with self.db.connect() as db:
            async with db.execute(query, (guild_id,)) as cursor:
                columns = [desc[0] for desc in cursor.description]
                rows = await cursor.fetchall()

                return [dict(zip(columns, row)) for row in rows]


class AddBirthdayScenario(BaseScenario):
    def __init__(self):
        self.db = DB()

    async def proceed(self, guild_id: int, user_id: int, birthday: str) -> bool:
        query = "INSERT INTO birthdays (guild_id, user_id, birthday, last_congrats) VALUES (?, ?, ?, ?)"
        async with self.db._write_lock:
            async with self.db.connect() as db:
                await db.execute(query, (guild_id, user_id, birthday, None))
                return True


class DeleteBirthdayScenario(BaseScenario):
    def __init__(self):
        self.db = DB()

    async def proceed(self, user_id: int, guild_id: int) -> bool:
        query = "DELETE FROM birthdays WHERE user_id = ? AND guild_id = ?"
        async with self.db._write_lock:
            async with self.db.connect() as cursor:
                await cursor.execute(query, (user_id, guild_id))
                return True


class ExistBirthdayCheckScenario(BaseScenario):
    def __init__(self):
        self.db = DB()

    async def proceed(self, user_id: int, guild_id: int):
        query = "SELECT * FROM birthdays WHERE user_id = ? AND guild_id = ?"
        async with self.db.connect() as cursor:
            await cursor.execute(query, (user_id, guild_id))
            return await cursor.fetchone()


class GetTodayBirthdayScenario(BaseScenario):
    def __init__(self):
        self.db = DB()

    async def proceed(self, guild_id: int, today: str):
        query = """SELECT user_id FROM birthdays WHERE guild_id = ?
                AND birthday = ? AND (last_congrats IS NULL OR last_congrats != ?"""
        async with self.db.connect() as cursor:
            await cursor.execute(query, (today, today))
            return await cursor.fetchall()


class UpdateLstCongratsScenario(BaseScenario):
    def __init__(self):
        self.db = DB()

    async def proceed(self, user_id: int, guild_id: int, date: str):
        query = "UPDATE birthdays SET last_congrats = ? WHERE user_id = ? AND guild_id = ?"
        async with self.db._write_lock:
            async with self.db.connect() as cursor:
                await cursor.execute(query, (date, user_id, guild_id))


class ResetAllCongratsScenario(BaseScenario):
    def __init__(self):
        self.db = DB()

    async def proceed(self):
        query = "UPDATE birthdays SET last_congrats = NULL"
        async with self.db._write_lock:
            async with self.db.connect() as cursor:
                await cursor.execute(query)
