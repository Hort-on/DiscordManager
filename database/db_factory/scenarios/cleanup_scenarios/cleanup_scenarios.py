from database.data_base_model import DB
from database.db_factory.scenarios.base_scenario import DataBaseScenario

from modules.logger.logger import Logger


class CleanupRemovedGuildScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            table_name: str,
            guild_id: int,
    ):
        super().__init__(
            db_connect,
            logger,
            guild_id
        )

        self.table_name = table_name

    async def _execute(self) -> None:
        async with self.db_connect.connect() as db:
            for table in self.table_map.values():
                query = f'DELETE FROM {table} WHERE guild_id = ?'

                await db.execute(query, (self.guild_id,))


class CleanupRemovedUserScenario(DataBaseScenario):
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

    async def _execute(self) -> None:
        async with self.db_connect.connect() as db:
            for table in self.USER_TABLES:
                query = f'DELETE FROM {table} WHERE guild_id = ? AND user_id = ?'

                await db.execute(query, (self.guild_id, self.user_id))


class CleanupRemovedChannelScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
            channel_id: int
    ):
        super().__init__(
            db_connect,
            logger,
            guild_id
        )

        self.channel_id = channel_id

    async def _execute(self) -> None:
        table = self._get_table('channels')
        query = f'DELETE FROM {table} WHERE guild_id = ? AND channel_id = ?'

        async with self.db_connect.connect() as db:
            await db.execute(query, (self.guild_id, self.channel_id))


class CleanupRemovedRoleScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
            role_id: int
    ):
        super().__init__(
            db_connect,
            logger,
            guild_id
        )

        self.role_id = role_id

    async def _execute(self) -> None:
        table = self._get_table('roles')
        query = f'DELETE FROM {table} WHERE guild_id = ? AND role_id = ?'

        async with self.db_connect.connect() as db:
            await db.execute(query, (self.guild_id, self.role_id))
