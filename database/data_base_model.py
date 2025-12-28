import asyncio

import aiosqlite
from contextlib import asynccontextmanager
from utils.messages import DB_MSGS as DM
from modules.logger.logger import Logger


class DB:
    def __init__(self, logger: Logger, path='database.sqlite'):
        self.logger = logger
        self.path = path

        self._write_lock = asyncio.Lock()

    @asynccontextmanager
    async def connect(self):
        async with self._write_lock:
            conn = await aiosqlite.connect(self.path)
            try:
                yield conn
                await conn.commit()
            finally:
                await conn.close()

    async def _create_all_tables(self):
        try:
            async with self.connect() as cursor:
                await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS GuildSettings (
                        guild_id INTEGER PRIMARY KEY,
                        birthday INTEGER NOT NULL DEFAULT 1,
                        congrats INTEGER NOT NULL DEFAULT 1,
                        congrats_channel_id INTEGER DEFAULT NULL,
    
                        verification INTEGER NOT NULL DEFAULT 1,
                        verification_channel_id INTEGER DEFAULT NULL,
                        verification_msg_id INTEGER DEFAULT NULL,
                        
                        system_channel_id INTEGER DEFAULT NULL,
    
                        block_users INTEGER NOT NULL DEFAULT 1,
                        invitation_checking INTEGER NOT NULL DEFAULT 1,
                        spam_check INTEGER NOT NULL DEFAULT 1,
                        member_left INTEGER NOT NULL DEFAULT 1,
                        send_messages INTEGER NOT NULL DEFAULT 1,
                        write_audit_log INTEGER NOT NULL DEFAULT 1,
                        role_manager INTEGER NOT NULL DEFAULT 1,
                        configuration_done INTEGER NOT NULL DEFAULT 0
                    )
                ''')

                await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS SuperUsers (
                        guild_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        PRIMARY KEY (guild_id, user_id)
                    );
                ''')

                await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS SelectedChannels (
                        guild_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        channel_id INTEGER NOT NULL,
                        PRIMARY KEY (guild_id, user_id)
                    );
                ''')

                await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Birthdays (
                        guild_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        birthday TEXT NOT NULL,
                        last_congrats TEXT,
                        PRIMARY KEY (guild_id, user_id)
                    );
                ''')

                await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS SpamInfo (
                        guild_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        user_warning_count INTEGER NOT NULL DEFAULT 0,
                        PRIMARY KEY (guild_id, user_id)
                    );
                ''')

                await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Roles (
                        guild_id INTEGER NOT NULL,
                        role_id INTEGER NOT NULL,
                        is_public INTEGER NOT NULL DEFAULT 1,
                        PRIMARY KEY (guild_id, role_id)
                    )
                ''')

        except Exception as e:
            await self.logger.error(DM.get('failure_create_table_msg'), exc=e)
