from database.data_base_model import DB
from database.db_factory.scenarios.base_scenario import DataBaseScenario

from modules.logger.logger import Logger


class GetDataScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
            table_name: str,
            *columns
    ):
        super().__init__(
            db_connect,
            logger,
            guild_id
        )

        self.table_name = table_name
        self.columns = columns

    async def _execute(self) -> dict:
        table = self._get_table(self.table_name)
        columns_sql = ', '.join(self.columns)
        query = f'SELECT {columns_sql} FROM {table} WHERE guild_id = ?'

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
        super().__init__(
            db_connect,
            logger,
            guild_id
        )

        self.table_name = table_name
        self.data = data

    async def _execute(self) -> bool:
        table = self._get_table(self.table_name)

        columns = ', '.join(['guild_id', *self.data.keys()])
        placeholders = ', '.join(['?'] * (len(self.data) + 1))
        update_clause = ', '.join(f'{k}=excluded.{k}' for k in self.data.keys())

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
        super().__init__(
            db_connect,
            logger,
            guild_id
        )

        self.table_name = table_name
        self.user_ids = user_ids

    async def _execute(self) -> bool:
        table = self._get_table('super_users')

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
        super().__init__(
            db_connect,
            logger,
            guild_id
        )

        self.table_name = table_name

    async def _execute(self) -> list[dict | None]:
        table = self._get_table(self.table_name)
        query = f'SELECT * FROM {table} WHERE guild_id = ?'

        async with self.db_connect.connect() as db:
            async with db.execute(query, (self.guild_id,)) as cursor:
                columns = [desc[0] for desc in cursor.description]
                rows = await cursor.fetchall()

                if not rows:
                    return []

                return [dict(zip(columns, row)) for row in rows]
