from database.data_base_model import DB

from services.factories.db_factory.scenarios.base import DataBaseScenario
from services.logger.logger import Logger


class CleanupGuild(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
    ):
        super().__init__(
            db_connect=db_connect,
            logger=logger,
            guild_id=guild_id
        )

    async def _execute(self) -> bool:
        async with self.db_connect.connect() as cursor:
            query = f'DELETE FROM GuildSettings WHERE guild_id = ?'
            await cursor.execute(query, (self.guild_id,))
            return cursor.total_changes > 0


class CleanupUser(DataBaseScenario):
    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int,
            user_ids: set[int]
    ):
        super().__init__(
            db_connect=db_connect,
            logger=logger,
            guild_id=guild_id
        )

        self.user_ids = user_ids

    async def _execute(self) -> bool:
        if not self.user_ids:
            return False

        placeholders = ', '.join('?' for _ in self.user_ids)

        async with self.db_connect.connect() as cursor:
            for table_key in self.USER_TABLES:
                table = self._get_table(table_key)

                query = f'''
                    DELETE FROM {table}
                    WHERE guild_id = ?
                      AND user_id IN ({placeholders})
                '''

                await cursor.execute(
                    query,
                    (self.guild_id, *self.user_ids)
                )

            return cursor.total_changes > 0


class CleanupSystemChannels(DataBaseScenario):
    def __init__(
        self,
        db_connect: DB,
        logger: Logger,
        guild_id: int,
        channels: list[str]
    ):
        super().__init__(db_connect, logger, guild_id)
        self.channels = channels

    async def _execute(self) -> bool:
        table = self._get_table('sys_channels')

        async with self.db_connect.connect() as cursor:
            for key in self.channels:
                query = (
                    f'UPDATE {table} '
                    f'SET {key} = NULL '
                    f'WHERE guild_id = ? '
                )
                await cursor.execute(query, (self.guild_id,))

            return cursor.total_changes > 0


class CleanUpVerificationRole(DataBaseScenario):
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
        query = (
            f'UPDATE GuildSettings'
            f'SET verification_role_id = NULL '
            f'WHERE guild_id = ? '
        )

        async with self.db_connect.connect() as cursor:
            await cursor.execute(query, (self.guild_id,))
