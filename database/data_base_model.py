import asyncio

import aiosqlite
from contextlib import asynccontextmanager

class DB:
    def __init__(self, path='database.sqlite'):
        self.path = path
        self._create_all_tables()
        self._write_lock = asyncio.Lock()


    @asynccontextmanager
    async def connect(self):
        conn = await aiosqlite.connect(self.path)
        try:
            yield conn
            await conn.commit()
        finally:
            await conn.close()

    async def _create_all_tables(self):
        async with self.connect() as cursor:
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS GuildSettings (
                    guild_id INTEGER PRIMARY KEY,
                    birthday BOOLEAN DEFAULT TRUE NOT NULL,
                    congrats BOOLEAN DEFAULT TRUE NOT NULL,
                    congrats_channel_id INTEGER DEFAULT NULL,

                    verification BOOLEAN DEFAULT TRUE NOT NULL,
                    verification_channel_id INTEGER DEFAULT NULL,
                    verification_msg_id INTEGER DEFAULT NULL,
                    
                    system_channel_id INTEGER DEFAULT NULL,

                    block_users BOOLEAN DEFAULT TRUE NOT NULL,
                    invitation_checking BOOLEAN DEFAULT TRUE NOT NULL,
                    spam_check BOOLEAN DEFAULT TRUE NOT NULL,
                    member_left BOOLEAN DEFAULT TRUE NOT NULL,
                    send_messages BOOLEAN DEFAULT TRUE NOT NULL,
                    write_audit_log BOOLEAN DEFAULT TRUE NOT NULL,
                    configuration_done BOOLEAN DEFAULT FALSE NOT NULL
                )
            ''')

            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS SuperUsers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    UNIQUE (guild_id, user_id)
                )
            ''')

            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS SelectedChannels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    channel_id INTEGER NOT NULL,
                    UNIQUE (guild_id, user_id)
                )
            ''')

            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS birthdays
                      (guild_id INTEGER NOT NULL,
                       user_id INTEGER,
                       birthday TEXT,
                       last_congrats TEXT,
                       UNIQUE (guild_id, user_id)
                )
            ''')

            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS SpamInfo (
                    guild_id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    user_warning_count INTEGER,
                    UNIQUE (guild_id, user_id)
                )
            ''')
