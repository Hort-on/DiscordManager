from database.data_base_model import DB
from database.db_factory.scenarios.base import DataBaseScenario
from general_services.logger.logger import Logger


class GetData(DataBaseScenario):
    def __init__(
        self,
        db_connect: DB,
        logger: Logger,
        guild_id: int,
        table_name: str,
        columns: tuple[str],
    ):
        super().__init__(db_connect=db_connect, logger=logger, guild_id=guild_id)

        self.table_name = table_name
        self.columns = columns

    async def _execute(self) -> dict | None:
        table = self._get_table(self.table_name)

        columns_sql = ", ".join(self.columns) if self.columns else "*"
        query = f"SELECT {columns_sql} FROM {table} WHERE guild_id = ?"

        async with self.db_connect.connect_read() as conn:
            async with conn.execute(query, (self.guild_id,)) as cursor:
                col_names = [desc[0] for desc in cursor.description]
                row = await cursor.fetchone()

                return dict(zip(col_names, row)) if row else None


class WriteData(DataBaseScenario):
    def __init__(
        self,
        db_connect: DB,
        logger: Logger,
        guild_id: int,
        table_name: str,
        data: dict[str, int | str],
    ):
        super().__init__(db_connect=db_connect, logger=logger, guild_id=guild_id)

        self.table_name = table_name
        self.data = data

    async def _execute(self) -> bool:
        table = self._get_table(self.table_name)

        columns = ", ".join(["guild_id", *self.data.keys()])
        placeholders = ", ".join(["?"] * (len(self.data) + 1))
        update_clause = ", ".join(f"{k}=excluded.{k}" for k in self.data.keys())

        if "user_id" in self.data:
            conflict_target = "guild_id, user_id"
        else:
            conflict_target = "guild_id"

        query = f"""
            INSERT INTO {table} ({columns})
            VALUES ({placeholders})
            ON CONFLICT({conflict_target})
            DO UPDATE SET {update_clause}
        """

        async with self.db_connect.connect_write() as cursor:
            await cursor.execute(query, (self.guild_id, *self.data.values()))
            return cursor.total_changes > 0


class InsertSet(DataBaseScenario):
    def __init__(
        self,
        db_connect: DB,
        logger: Logger,
        guild_id: int,
        table_name: str,
        key: str,
        values: set[int],
    ):
        super().__init__(db_connect=db_connect, logger=logger, guild_id=guild_id)

        self.table_name = table_name
        self.key = key
        self.values = values

    async def _execute(self) -> bool:
        if not self.values:
            return False

        table = self._get_table(self.table_name)

        query = f"""
            INSERT OR IGNORE INTO {table} (guild_id, {self.key})
            VALUES (?, ?)
        """

        params = [(self.guild_id, v) for v in self.values]

        async with self.db_connect.connect_write() as cursor:
            await cursor.executemany(query, params)
            return cursor.total_changes > 0


class DeleteSet(DataBaseScenario):
    def __init__(
        self,
        db_connect: DB,
        logger: Logger,
        guild_id: int,
        table_name: str,
        key: str,
        values: set[int],
    ):
        super().__init__(db_connect=db_connect, logger=logger, guild_id=guild_id)

        self.table_name = table_name
        self.key = key
        self.values = values

    async def _execute(self) -> bool:
        if not self.values:
            return False

        table = self._get_table(self.table_name)
        placeholders = ", ".join("?" for _ in self.values)

        query = f"""
            DELETE FROM {table}
            WHERE guild_id = ?
              AND {self.key} IN ({placeholders})
        """

        params = (self.guild_id, *self.values)

        async with self.db_connect.connect_write() as cursor:
            await cursor.execute(query, params)
            return cursor.total_changes > 0


class FetchAllData(DataBaseScenario):
    def __init__(self, db_connect: DB, logger: Logger, guild_id: int, table_name: str):
        super().__init__(db_connect=db_connect, logger=logger, guild_id=guild_id)

        self.table_name = table_name

    async def _execute(self) -> list[dict | None]:
        table = self._get_table(self.table_name)
        query = f"SELECT * FROM {table} WHERE guild_id = ?"

        async with self.db_connect.connect_read() as conn:
            async with conn.execute(query, (self.guild_id,)) as cursor:
                columns = [desc[0] for desc in cursor.description]
                rows = await cursor.fetchall()

                if not rows:
                    return []

                return [dict(zip(columns, row)) for row in rows]


class InitGuild(DataBaseScenario):
    def __init__(self, db_connect: DB, logger: Logger, guild_id: int):
        super().__init__(db_connect=db_connect, logger=logger, guild_id=guild_id)

    async def _execute(self):
        async with self.db_connect.connect_write() as db:
            await db.execute(
                "INSERT OR IGNORE INTO GuildSettings (guild_id) VALUES (?)",
                (self.guild_id,),
            )

            await db.execute(
                "INSERT OR IGNORE INTO SystemChannels (guild_id) VALUES (?)",
                (self.guild_id,),
            )
