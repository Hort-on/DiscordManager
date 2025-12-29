from database.data_base_model import DB
from modules.logger.logger import Logger
from utils.messages import DB_MSGS as DM


class DataBaseScenario:
    table_map = {
        'settings': "GuildSettings",
        'super_users': "SuperUsers",
        'channels': "SelectedChannels",
        'birthdays': "Birthdays"
    }

    def __init__(self, db_connect: DB, logger: Logger):
        self.logger = logger
        self.db_connect = db_connect

    async def db_proceed(self):
        try:
            return await self._execute()
        except Exception as e:
            await self.logger.error(
                await self.logger.error(DM.get('failure_read_msg'), exc=e)
            )
            return None

    async def _execute(self):
        raise NotImplementedError

    def _get_table(self, table_name: str) -> str:
        table = self.table_map.get(table_name)
        if not table:
            raise ValueError(f"Unknown table name: {table_name}")
        return table



class GetDataScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
            table_name: str,
            *columns
    ):
        super().__init__(db_connect, logger)

        self.db_connect = db_connect
        self.guild_id = guild_id
        self.table_name = table_name
        self.columns = columns

    async def _execute(self) -> dict:
        table = self._get_table(self.table_name)
        columns_sql = ", ".join(self.columns)
        query = f"SELECT {columns_sql} FROM {table} WHERE guild_id = ?"


        async with self.db_connect.connect() as db:
            async with db.execute(query, (self.guild_id,)) as cursor:
                col_names = [desc[0] for desc in cursor.description]

                row = await cursor.fetchone()
                return dict(zip(col_names, row)) if row else None



class WriteDataScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
            table_name: str,
            data: dict
    ):
        super().__init__(db_connect, logger)

        self.db_connect = db_connect
        self.guild_id = guild_id
        self.table_name = table_name
        self.data = data

    async def _execute(self) -> bool:
        table = self._get_table(self.table_name)

        columns = ", ".join(["guild_id", *self.data.keys()])
        placeholders = ", ".join(["?"] * (len(self.data) + 1))
        update_clause = ", ".join(f"{k}=excluded.{k}" for k in self.data.keys())

        query = f"""INSERT INTO {table} ({columns}) VALUES ({placeholders})
                            ON CONFLICT(guild_id) DO UPDATE SET {update_clause}"""

        async with self.db_connect.connect() as cursor:
            await cursor.execute(query, (self.guild_id, *self.data.values()))
            return cursor.rowcount > 0


class WriteUserScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
            table_name: str,
            user_ids: list[int]
    ):
        super().__init__(db_connect, logger)
        self.guild_id = guild_id
        self.table_name = table_name
        self.user_ids = user_ids

    async def _execute(self) -> bool:
        table = self._get_table("super_users")

        query = f"""
            INSERT INTO {table} (guild_id, user_id)
            VALUES (?, ?)
            ON CONFLICT(guild_id, user_id) DO NOTHING
        """

        values = [(self.guild_id, user_id) for user_id in self.user_ids]

        async with self.db_connect.connect() as cursor:
            await cursor.executemany(query, values)
            return cursor.rowcount > 0


class FetchAllDataScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
            table_name: str
    ):
        super().__init__(db_connect, logger)

        self.db_connect = db_connect
        self.guild_id = guild_id
        self.table_name = table_name

    async def _execute(self) -> list[dict | None]:
        table = self._get_table(self.table_name)
        query = f"SELECT * FROM {table} WHERE guild_id = ?"

        async with self.db_connect.connect() as db:
            async with db.execute(query, (self.guild_id,)) as cursor:
                columns = [desc[0] for desc in cursor.description]
                rows = await cursor.fetchall()

                if not rows:
                    return []

                return [dict(zip(columns, row)) for row in rows]


class AddBirthdayScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
            user_id: int,
            user_birthday: str
    ):
        super().__init__(db_connect, logger)

        self.db_connect = db_connect
        self.guild_id = guild_id
        self.user_id = user_id
        self.birthday = user_birthday

    async def _execute(self) -> bool:
        table = self._get_table("birthdays")
        query = f"INSERT INTO {table} (guild_id, user_id, birthday, last_congrats) VALUES (?, ?, ?, ?)"

        async with self.db_connect.connect() as cursor:
            await cursor.execute(query, (self.guild_id, self.user_id, self.birthday, None))
            return cursor.rowcount > 0


class DeleteBirthdayScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
            user_id: int
    ):
        super().__init__(db_connect, logger)

        self.db_connect = db_connect
        self.guild_id = guild_id
        self.user_id = user_id

    async def _execute(self) -> bool:
        table = self._get_table("birthdays")
        query = f"DELETE FROM {table} WHERE guild_id = ? AND user_id = ?"

        async with self.db_connect.connect() as cursor:
            await cursor.execute(query, (self.guild_id, self.user_id))
            return cursor.rowcount > 0


class ExistBirthdayCheckScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
            user_id: int
    ):
        super().__init__(db_connect, logger)

        self.db_connect = db_connect
        self.guild_id = guild_id
        self.user_id = user_id

    async def _execute(self) -> bool:
        table = self._get_table("birthdays")
        query = f"SELECT 1 FROM {table} WHERE user_id = ? AND guild_id = ? LIMIT 1"

        async with self.db_connect.connect() as cursor:
            await cursor.execute(query, (self.user_id, self.guild_id))
            return await cursor.fetchone() is not None

class GetTodayBirthdayScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
            today: str
    ):
        super().__init__(db_connect, logger)

        self.db_connect = db_connect
        self.guild_id = guild_id
        self.today = today

    async def _execute(self) -> list[int]:
        table = self._get_table("birthdays")
        query = f"""SELECT user_id FROM {table} WHERE guild_id = ?
                AND birthday = ? AND (last_congrats IS NULL OR last_congrats != ?)"""

        async with self.db_connect.connect() as cursor:
            await cursor.execute(query, (self.guild_id, self.today, self.today))
            return await cursor.fetchall()


class UpdateLastCongratsScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
            user_id: int,
            today_str: str
    ):
        super().__init__(db_connect, logger)

        self.db_connect = db_connect
        self.guild_id = guild_id
        self.user_id = user_id
        self.date = today_str

    async def _execute(self) -> bool:
        table = self._get_table("birthdays")
        query = f"UPDATE {table} SET last_congrats = ? WHERE user_id = ? AND guild_id = ?"

        async with self.db_connect.connect() as cursor:
            await cursor.execute(query, (self.date, self.user_id, self.guild_id))
            return cursor.rowcount > 0


class ResetAllCongratsScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger
    ):
        super().__init__(db_connect, logger)
        self.db_connect = db_connect
        self.logger = logger

    async def _execute(self) -> None:
        table = self._get_table("birthdays")
        query = f"UPDATE {table} SET last_congrats = NULL"

        async with self.db_connect.connect() as cursor:
            await cursor.execute(query)
