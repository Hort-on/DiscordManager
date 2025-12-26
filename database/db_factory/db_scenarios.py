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


    async def proceed(self):
        raise NotImplementedError


class GetDataScenario(BaseScenario):
    def __init__(self, guild_id, table_name, columns):
        super().__init__()
        self.db = DB()
        self.guild_id = guild_id
        self.table_name = table_name
        self.columns = columns

    async def proceed(self) -> dict | None:
        table = self._get_table(self.table_name)
        columns_sql = ", ".join(self.columns) if self.columns else "*"
        query = f"SELECT {columns_sql} FROM {table} WHERE guild_id = ?"

        async with self.db.connect() as db:
            async with db.execute(query, (self.guild_id,)) as cursor:
                col_names = [desc[0] for desc in cursor.description]

                row = await cursor.fetchone()
                return dict(zip(col_names, row)) if row else None


class WriteDataScenario(BaseScenario):
    def __init__(self, guild_id: int, table_name: str, data: dict):
        super().__init__()
        self.db = DB()
        self.guild_id = guild_id
        self.table_name = table_name
        self.data = data

    async def proceed(self) -> bool:
        table = self._get_table(self.table_name)

        async with self.db.connect() as cursor:
            columns = ", ".join(["guild_id", *self.data.keys()])
            placeholders = ", ".join(["?"] * (len(self.data) + 1))
            update_clause = ", ".join(f"{k}=excluded.{k}" for k in self.data.keys())
            query = f"""INSERT INTO {table} ({columns}) VALUES ({placeholders})
                    ON CONFLICT(guild_id) DO UPDATE SET {update_clause}"""

            await cursor.execute(query, (self.guild_id, *self.data.values()))
            return cursor.rowcount > 0

class FetchAllDataScenario(BaseScenario):
    def __init__(self, guild_id: int, table_name: str):
        super().__init__()
        self.db = DB()
        self.guild_id = guild_id
        self.table_name = table_name

    async def proceed(self) -> list[dict | None]:
        table = self._get_table(self.table_name)
        query = f"SELECT * FROM {table} WHERE guild_id = ?"

        async with self.db.connect() as db:
            async with db.execute(query, (self.guild_id,)) as cursor:
                columns = [desc[0] for desc in cursor.description]
                rows = await cursor.fetchall()

                if not rows:
                    return []

                return [dict(zip(columns, row)) for row in rows]


class AddBirthdayScenario(BaseScenario):
    def __init__(self, guild_id: int, user_id: int, user_birthday: str):
        self.db = DB()
        self.guild_id = guild_id
        self.user_id = user_id
        self.birthday = user_birthday

    async def proceed(self) -> bool:
        table = self._get_table("birthdays")
        query = f"INSERT INTO {table} (guild_id, user_id, birthday, last_congrats) VALUES (?, ?, ?, ?)"
        async with self.db.connect() as cursor:
            await cursor.execute(query, (self.guild_id, self.user_id, self.birthday, None))
            return cursor.rowcount > 0


class DeleteBirthdayScenario(BaseScenario):
    def __init__(self, guild_id: int, user_id: int):
        self.db = DB()
        self.guild_id = guild_id
        self.user_id = user_id

    async def proceed(self) -> bool:
        table = self._get_table("birthdays")
        query = f"DELETE FROM {table} WHERE guild_id = ? AND user_id = ?"
        async with self.db.connect() as cursor:
            await cursor.execute(query, (self.guild_id, self.user_id))
            return cursor.rowcount > 0


class ExistBirthdayCheckScenario(BaseScenario):
    def __init__(self, guild_id: int, user_id: int):
        self.db = DB()
        self.guild_id = guild_id
        self.user_id = user_id

    async def proceed(self) -> bool:
        table = self._get_table("birthdays")
        query = f"SELECT 1 FROM {table} WHERE user_id = ? AND guild_id = ? LIMIT 1"
        async with self.db.connect() as cursor:
            await cursor.execute(query, (self.user_id, self.guild_id))
            return await cursor.fetchone() is not None


class GetTodayBirthdayScenario(BaseScenario):
    def __init__(self, guild_id: int, today: str):
        self.db = DB()
        self.guild_id = guild_id
        self.today = today

    async def proceed(self) -> list[int]:
        # TODO: питання до того як цей запит працює
        table = self._get_table("birthdays")
        query = f"""SELECT user_id FROM {table} WHERE guild_id = ?
                AND birthday = ? AND (last_congrats IS NULL OR last_congrats != ?)"""
        async with self.db.connect() as cursor:
            await cursor.execute(query, (self.guild_id, self.today, self.today))
            return await cursor.fetchall()


class UpdateLstCongratsScenario(BaseScenario):
    def __init__(self, guild_id: int, user_id: int, today_str: str):
        self.db = DB()
        self.guild_id = guild_id
        self.user_id = user_id
        self.date = today_str

    async def proceed(self) -> bool:
        table = self._get_table("birthdays")
        query = f"UPDATE {table} SET last_congrats = ? WHERE user_id = ? AND guild_id = ?"
        async with self.db.connect() as cursor:
            await cursor.execute(query, (self.date, self.user_id, self.guild_id))
            return cursor.rowcount > 0


class ResetAllCongratsScenario(BaseScenario):
    def __init__(self):
        self.db = DB()

    async def proceed(self) -> None:
        table = self._get_table("birthdays")
        query = f"UPDATE {table} SET last_congrats = NULL"
        async with self.db.connect() as cursor:
            await cursor.execute(query)
