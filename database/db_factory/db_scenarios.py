from database.data_base_model import DB
from modules.logger.logger import Logger
from utils.messages import DB_MSGS as DM


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

    async def db_proceed(self):
        raise NotImplementedError


class GetDataScenario(BaseScenario):
    def __init__(
            self,
            logger: Logger,
            guild_id: int,
            table_name: str,
            *columns
    ):

        self.logger = logger
        self.db = DB(self.logger)
        self.guild_id = guild_id
        self.table_name = table_name
        self.columns = columns

    async def db_proceed(self) -> dict | None:
        table = self._get_table(self.table_name)
        columns_sql = ", ".join(self.columns)
        query = f"SELECT {columns_sql} FROM {table} WHERE guild_id = ?"

        try:
            async with self.db.connect() as db:
                async with db.execute(query, (self.guild_id,)) as cursor:
                    col_names = [desc[0] for desc in cursor.description]

                    row = await cursor.fetchone()
                    return dict(zip(col_names, row)) if row else None

        except Exception as e:
            await self.logger.error(DM.get('failure_read_msg'), exc=e)


class WriteDataScenario(BaseScenario):
    def __init__(
            self,
            logger: Logger,
            guild_id: int,
            table_name: str,
            data: dict
    ):

        self.logger = logger
        self.db = DB(self.logger)
        self.guild_id = guild_id
        self.table_name = table_name
        self.data = data

    async def db_proceed(self) -> bool | None:
        table = self._get_table(self.table_name)

        try:
            async with self.db.connect() as cursor:
                columns = ", ".join(["guild_id", *self.data.keys()])
                placeholders = ", ".join(["?"] * (len(self.data) + 1))
                update_clause = ", ".join(f"{k}=excluded.{k}" for k in self.data.keys())
                query = f"""INSERT INTO {table} ({columns}) VALUES ({placeholders})
                        ON CONFLICT(guild_id) DO UPDATE SET {update_clause}"""

                await cursor.execute(query, (self.guild_id, *self.data.values()))
                return cursor.rowcount > 0

        except Exception as e:
            await self.logger.error(DM.get('failure_write_msg'), exc=e)

class FetchAllDataScenario(BaseScenario):
    def __init__(
            self,
            logger: Logger,
            guild_id: int,
            table_name: str
    ):

        self.logger = logger
        self.db = DB(self.logger)
        self.guild_id = guild_id
        self.table_name = table_name

    async def db_proceed(self) -> list[dict | None] | None:
        table = self._get_table(self.table_name)
        query = f"SELECT * FROM {table} WHERE guild_id = ?"

        try:
            async with self.db.connect() as db:
                async with db.execute(query, (self.guild_id,)) as cursor:
                    columns = [desc[0] for desc in cursor.description]
                    rows = await cursor.fetchall()

                    if not rows:
                        return []

                    return [dict(zip(columns, row)) for row in rows]

        except Exception as e:
            await self.logger.error(DM.get('failure_read_msg', exc=e))


class AddBirthdayScenario(BaseScenario):
    def __init__(
            self,
            logger: Logger,
            guild_id: int,
            user_id: int,
            user_birthday: str
    ):

        self.logger = logger
        self.db = DB(self.logger)
        self.guild_id = guild_id
        self.user_id = user_id
        self.birthday = user_birthday

    async def db_proceed(self) -> bool | None:
        table = self._get_table("birthdays")
        query = f"INSERT INTO {table} (guild_id, user_id, birthday, last_congrats) VALUES (?, ?, ?, ?)"

        try:
            async with self.db.connect() as cursor:
                await cursor.execute(query, (self.guild_id, self.user_id, self.birthday, None))
                return cursor.rowcount > 0

        except Exception as e:
            await self.logger.error(DM.get('failure_write_msg', exc=e))


class DeleteBirthdayScenario(BaseScenario):
    def __init__(
            self,
            logger: Logger,
            guild_id: int,
            user_id: int
    ):

        self.logger = logger
        self.db = DB(self.logger)
        self.guild_id = guild_id
        self.user_id = user_id

    async def db_proceed(self) -> bool | None:
        table = self._get_table("birthdays")
        query = f"DELETE FROM {table} WHERE guild_id = ? AND user_id = ?"

        try:
            async with self.db.connect() as cursor:
                await cursor.execute(query, (self.guild_id, self.user_id))
                return cursor.rowcount > 0

        except Exception as e:
            await self.logger.error(DM.get('failure_write_msg'), exc=e)


class ExistBirthdayCheckScenario(BaseScenario):
    def __init__(
            self,
            logger: Logger,
            guild_id: int,
            user_id: int
    ):

        self.logger = logger
        self.db = DB(self.logger)
        self.guild_id = guild_id
        self.user_id = user_id

    async def db_proceed(self) -> bool | None:
        table = self._get_table("birthdays")
        query = f"SELECT 1 FROM {table} WHERE user_id = ? AND guild_id = ? LIMIT 1"

        try:
            async with self.db.connect() as cursor:
                await cursor.execute(query, (self.user_id, self.guild_id))
                return await cursor.fetchone() is not None

        except Exception as e:
            await self.logger.error(DM.get('failure_read_msg'), exc=e)

class GetTodayBirthdayScenario(BaseScenario):
    def __init__(
            self,
            logger: Logger,
            guild_id: int,
            today: str
    ):

        self.logger = logger
        self.db = DB(self.logger)
        self.guild_id = guild_id
        self.today = today

    async def db_proceed(self) -> list[int] | None:
        table = self._get_table("birthdays")
        query = f"""SELECT user_id FROM {table} WHERE guild_id = ?
                AND birthday = ? AND (last_congrats IS NULL OR last_congrats != ?)"""

        try:
            async with self.db.connect() as cursor:
                await cursor.execute(query, (self.guild_id, self.today, self.today))
                return await cursor.fetchall()

        except Exception as e:
            await self.logger.error(DM.get('failure_read_msg'), exc=e)


class UpdateLastCongratsScenario(BaseScenario):
    def __init__(
            self,
            logger: Logger,
            guild_id: int,
            user_id: int,
            today_str: str
    ):

        self.logger = logger
        self.db = DB(self.logger)
        self.guild_id = guild_id
        self.user_id = user_id
        self.date = today_str

    async def db_proceed(self) -> bool | None:
        table = self._get_table("birthdays")
        query = f"UPDATE {table} SET last_congrats = ? WHERE user_id = ? AND guild_id = ?"

        try:
            async with self.db.connect() as cursor:
                await cursor.execute(query, (self.date, self.user_id, self.guild_id))
                return cursor.rowcount > 0

        except Exception as e:
            await self.logger.error(DM.get('failure_write_msg'), exc=e)


class ResetAllCongratsScenario(BaseScenario):
    def __init__(
            self,
            logger: Logger
    ):

        self.logger = logger
        self.db = DB(self.logger)

    async def db_proceed(self) -> None:
        table = self._get_table("birthdays")
        query = f"UPDATE {table} SET last_congrats = NULL"

        try:
            async with self.db.connect() as cursor:
                await cursor.execute(query)

        except Exception as e:
            await self.logger.error(DM.get('failure_write_msg'), exc=e)
