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

#TODO: треба ще двоести до пуття
class GetDataScenario(BaseScenario):
    def __init__(self, guild_id, table_name, columns):
        super().__init__()
        self.db = DB()
        self.guild_id = guild_id
        self.table_name = table_name
        self.columns = columns

    async def proceed(self) -> dict | None:
        table = self._get_table(self.table_name)
        columns_sql = ", ".join(self.columns)
        query = f"SELECT {columns_sql} FROM {table} WHERE guild_id = ?"

        async with self.db.connect() as db:
            async with db.execute(query, self.guild_id) as cursor:
                col_names = [desc[0] for desc in cursor.description]

                row = await cursor.fetchone()
                return dict(zip(col_names, row)) if row else None


class WriteDataScenario(BaseScenario):
    def __init__(self):
        super().__init__()
        self.db = DB()

    async def proceed(self, guild_id: int, table_name: str, data: dict) -> bool:
        table = self._get_table(table_name)

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
    def __init__(self, guild_id: int, user_id: int, user_birthday: str):
        self.db = DB()
        self.guild_id = guild_id
        self.user_id = user_id
        self.birthday = user_birthday

    async def proceed(self) -> bool:
        query = "INSERT INTO birthdays (guild_id, user_id, birthday, last_congrats) VALUES (?, ?, ?, ?)"
        async with self.db.connect() as db:
            await db.execute(query, (self.guild_id, self.user_id, self.birthday, None))
            return True


class DeleteBirthdayScenario(BaseScenario):
    def __init__(self, guild_id: int, user_id: int):
        self.db = DB()
        self.guild_id = guild_id
        self.user_id = user_id

    async def proceed(self) -> bool:
        query = "DELETE FROM birthdays WHERE user_id = ? AND guild_id = ?"
        async with self.db.connect() as cursor:
            await cursor.execute(query, (self.user_id, self.guild_id))
            return True


class ExistBirthdayCheckScenario(BaseScenario):
    def __init__(self, guild_id: int, user_id: int):
        self.db = DB()
        self.guild_id = guild_id
        self.user_id = user_id

    async def proceed(self) -> tuple | None:
        query = "SELECT * FROM birthdays WHERE user_id = ? AND guild_id = ?"
        async with self.db.connect() as cursor:
            await cursor.execute(query, (self.user_id, self.guild_id))
            return await cursor.fetchone()


class GetTodayBirthdayScenario(BaseScenario):
    def __init__(self, guild_id: int, today: str):
        self.db = DB()
        self.guild_id = guild_id
        self.today = today

    async def proceed(self) -> list[tuple] | None:
        # TODO: питання до того як цей запит працює
        query = """SELECT user_id FROM birthdays WHERE guild_id = ?
                AND birthday = ? AND (last_congrats IS NULL OR last_congrats != ?"""
        async with self.db.connect() as cursor:
            await cursor.execute(query, (self.guild_id, self.today, self.today))
            return await cursor.fetchall()


class UpdateLstCongratsScenario(BaseScenario):
    def __init__(self, guild_id: int, user_id: int, today_str: str):
        self.db = DB()
        self.guild_id = guild_id
        self.user_id = user_id
        self.date = today_str

    async def proceed(self) -> None:
        query = "UPDATE birthdays SET last_congrats = ? WHERE user_id = ? AND guild_id = ?"
        async with self.db.connect() as cursor:
            await cursor.execute(query, (self.date, self.user_id, self.guild_id))


class ResetAllCongratsScenario(BaseScenario):
    def __init__(self):
        self.db = DB()

    async def proceed(self) -> None:
        query = "UPDATE birthdays SET last_congrats = NULL"
        async with self.db.connect() as cursor:
            await cursor.execute(query)
