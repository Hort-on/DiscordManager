from __future__ import annotations

from database.data_base_model import DB
from database.db_factory.scenarios.base import DataBaseScenario
from general_services.logger.logger import Logger


class SaveTempChannelScenario(DataBaseScenario):
    def __init__(
        self,
        db_connect: DB,
        logger: Logger,
        guild_id: int,
        channel_id: int,
        owner_id: int,
    ):
        super().__init__(db_connect=db_connect, logger=logger, guild_id=guild_id)

        self.channel_id = channel_id
        self.owner_id = owner_id

    async def _execute(self) -> bool:
        table = self._get_table("temp_channels")
        query = f"""
            INSERT OR REPLACE INTO {table} (guild_id, channel_id, owner_id)
            VALUES (?, ?, ?)
        """

        async with self.db_connect.connect_write() as cursor:
            await cursor.execute(query, (self.guild_id, self.channel_id, self.owner_id))
            return cursor.total_changes > 0


class GetTempChannelByOwnerScenario(DataBaseScenario):
    def __init__(self, db_connect: DB, logger: Logger, guild_id: int, owner_id: int):
        super().__init__(db_connect=db_connect, logger=logger, guild_id=guild_id)

        self.owner_id = owner_id

    async def _execute(self) -> dict | None:
        table = self._get_table("temp_channels")
        query = f"""
            SELECT guild_id, channel_id, owner_id
            FROM {table}
            WHERE guild_id = ?
              AND owner_id = ?
            LIMIT 1
        """

        async with self.db_connect.connect_read() as conn:
            async with conn.execute(query, (self.guild_id, self.owner_id)) as cursor:
                row = await cursor.fetchone()

                if not row:
                    return None

                return {
                    "guild_id": row[0],
                    "channel_id": row[1],
                    "owner_id": row[2],
                }


class GetTempChannelScenario(DataBaseScenario):
    def __init__(self, db_connect: DB, logger: Logger, guild_id: int, channel_id: int):
        super().__init__(db_connect=db_connect, logger=logger, guild_id=guild_id)

        self.channel_id = channel_id

    async def _execute(self) -> dict | None:
        table = self._get_table("temp_channels")
        query = f"""
            SELECT guild_id, channel_id, owner_id
            FROM {table}
            WHERE guild_id = ?
              AND channel_id = ?
            LIMIT 1
        """

        async with self.db_connect.connect_read() as conn:
            async with conn.execute(query, (self.guild_id, self.channel_id)) as cursor:
                row = await cursor.fetchone()

                if not row:
                    return None

                return {
                    "guild_id": row[0],
                    "channel_id": row[1],
                    "owner_id": row[2],
                }


class DeleteTempChannelScenario(DataBaseScenario):
    def __init__(self, db_connect: DB, logger: Logger, guild_id: int, channel_id: int):
        super().__init__(db_connect=db_connect, logger=logger, guild_id=guild_id)

        self.channel_id = channel_id

    async def _execute(self) -> bool:
        table = self._get_table("temp_channels")
        query = f"""
            DELETE FROM {table}
            WHERE guild_id = ?
              AND channel_id = ?
        """

        async with self.db_connect.connect_write() as cursor:
            await cursor.execute(query, (self.guild_id, self.channel_id))
            return cursor.total_changes > 0
