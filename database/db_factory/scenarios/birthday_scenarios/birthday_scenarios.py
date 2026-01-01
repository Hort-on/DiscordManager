from database.data_base_model import DB
from database.db_factory.db_scenarios import DataBaseScenario

from modules.logger.logger import Logger


class AddBirthdayScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
            user_id: int,
            user_birthday: str
    ):
        super().__init__(
            db_connect,
            logger,
            guild_id
        )

        self.user_id = user_id
        self.birthday = user_birthday

    async def _execute(self) -> bool:
        table = self._get_table('birthdays')
        query = f'INSERT INTO {table} (guild_id, user_id, birthday, last_congrats) VALUES (?, ?, ?, ?)'

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
        super().__init__(
            db_connect,
            logger,
            guild_id
        )

        self.user_id = user_id

    async def _execute(self) -> bool:
        table = self._get_table('birthdays')
        query = f'DELETE FROM {table} WHERE guild_id = ? AND user_id = ?'

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
        super().__init__(
            db_connect,
            logger,
            guild_id
        )

        self.user_id = user_id

    async def _execute(self) -> bool:
        table = self._get_table('birthdays')
        query = f'SELECT 1 FROM {table} WHERE user_id = ? AND guild_id = ? LIMIT 1'

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
        super().__init__(
            db_connect,
            logger,
            guild_id
        )

        self.today = today

    async def _execute(self) -> list[int]:
        table = self._get_table('birthdays')
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
        super().__init__(
            db_connect,
            logger,
            guild_id
        )

        self.user_id = user_id
        self.date = today_str

    async def _execute(self) -> bool:
        table = self._get_table('birthdays')
        query = f'UPDATE {table} SET last_congrats = ? WHERE user_id = ? AND guild_id = ?'

        async with self.db_connect.connect() as cursor:
            await cursor.execute(query, (self.date, self.user_id, self.guild_id))
            return cursor.rowcount > 0


class ResetAllCongratsScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger
    ):
        super().__init__(
            db_connect,
            logger,
            guild_id=None
        )

        self.logger = logger

    async def _execute(self) -> None:
        table = self._get_table('birthdays')
        query = f'UPDATE {table} SET last_congrats = NULL'

        async with self.db_connect.connect() as cursor:
            await cursor.execute(query)
