from database.data_base_model import DB

from services.factories.db_factory.scenarios.base import DataBaseScenario
from services.logger.logger import Logger


class CleanupRemovedGuildScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
    ):
        super().__init__(
            db_connect,
            logger,
            guild_id
        )

    async def _execute(self) -> None:
        async with self.db_connect.connect() as cursor:
            query = f'DELETE FROM GuildSettings WHERE guild_id = ?'
            await cursor.execute(query, (self.guild_id,))


class CleanupRemovedUserScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
            user_ids: set[int]
    ):
        super().__init__(
            db_connect,
            logger,
            guild_id
        )

        self.user_ids = user_ids

    async def _execute(self) -> None:
        if not self.user_ids:
            return

        placeholders = ','.join('?' for _ in self.user_ids)

        async with self.db_connect.connect() as cursor:
            for table in self.USER_TABLES:
                query = f'''
                    DELETE FROM {table}
                    WHERE guild_id = ?
                    AND user_id IN ({placeholders})
                '''

                params = (self.guild_id, *self.user_ids)
                await cursor.execute(query, params)


class CleanupRemovedChannelScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
            channel_ids: set[int]
    ):
        super().__init__(
            db_connect,
            logger,
            guild_id
        )

        self.channel_ids = channel_ids

    async def _execute(self) -> None:
        if not self.channel_ids:
            return

        table = self._get_table('channels')

        placeholders = ','.join('?' for _ in self.channel_ids)
        query = (
            f'DELETE FROM {table} '
            f'WHERE guild_id = ? '
            f'AND channel_id IN ({placeholders})'
        )

        params = (self.guild_id, *self.channel_ids)

        async with self.db_connect.connect() as cursor:
            await cursor.execute(query, params)


class CleanupRemovedRoleScenario(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
            role_ids: set[int]
    ):
        super().__init__(
            db_connect,
            logger,
            guild_id
        )

        self.role_ids = role_ids

    async def _execute(self) -> None:
        if not self.role_ids:
            return

        table = self._get_table('roles')

        placeholders = ','.join('?' for _ in self.role_ids)
        query = (
            f'DELETE FROM {table} '
            f'WHERE guild_id = ? '
            f'AND role_id IN ({placeholders})'
        )

        params = (self.guild_id, *self.role_ids)

        async with self.db_connect.connect() as cursor:
            await cursor.execute(query, params)
