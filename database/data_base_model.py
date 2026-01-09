import asyncio
import aiosqlite
from contextlib import asynccontextmanager
from services.utils.messages import DB_MSGS as DM
from modules.logger.logger import Logger


class DB:
    def __init__(self, logger: Logger, path='database.DATA.sqlite'):
        self.logger = logger
        self.path = path
        self._write_lock = asyncio.Lock()
        asyncio.create_task(self._init_tables())

    async def _init_tables(self):
        async with self._write_lock:
            temp_conn = await aiosqlite.connect(self.path)
            await temp_conn.execute("PRAGMA foreign_keys = ON")
            try:
                await temp_conn.execute('''
                    CREATE TABLE IF NOT EXISTS GuildSettings (
                        guild_id INTEGER PRIMARY KEY,
                    
                        birthday INTEGER NOT NULL DEFAULT 0,
                        congrats INTEGER NOT NULL DEFAULT 0,
                        congrats_channel_id INTEGER,
                    
                        verification INTEGER NOT NULL DEFAULT 0,
                        verification_channel_id INTEGER DEFAULT NULL,
                        verification_msg_id INTEGER DEFAULT NULL,
                    
                        notification_channel_id INTEGER DEFAULT NULL,
                    
                        block_users INTEGER NOT NULL DEFAULT 0,
                        invitation_checking INTEGER NOT NULL DEFAULT 0,
                        spam_check INTEGER NOT NULL DEFAULT 0,
                        member_left INTEGER NOT NULL DEFAULT 0,
                    
                        send_messages INTEGER NOT NULL DEFAULT 1,
                        write_audit_log INTEGER NOT NULL DEFAULT 1,
                        role_manager INTEGER NOT NULL DEFAULT 0
                    );
                ''')

                await temp_conn.execute('''
                    CREATE TABLE IF NOT EXISTS GuildSelectedChannels (
                        guild_id INTEGER PRIMARY KEY,
                        
                        congrats_channel_id INTEGER DEFAULT NULL,
                        verification_channel_id INTEGER DEFAULT NULL,
                        notification_channel_id INTEGER DEFAULT NULL,
                        
                        FOREIGN KEY (guild_id)
                            REFERENCES GuildSettings(guild_id)
                            ON DELETE CASCADE
                    );
                ''')

                await temp_conn.execute('''
                    CREATE TABLE IF NOT EXISTS HiddenChannels (
                        guild_id INTEGER NOT NULL,
                        channel_id INTEGER NOT NULL,
                    
                        PRIMARY KEY (guild_id, channel_id),
                    
                        FOREIGN KEY (guild_id)
                            REFERENCES GuildSettings(guild_id)
                            ON DELETE CASCADE
                    );
                ''')

                await temp_conn.execute('''
                    CREATE TABLE IF NOT EXISTS ChannelsToSend (
                        guild_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        channel_id INTEGER NOT NULL,

                        PRIMARY KEY (guild_id, user_id),

                        FOREIGN KEY (guild_id)
                            REFERENCES GuildSettings(guild_id)
                            ON DELETE CASCADE
                    );
                ''')

                await temp_conn.execute('''
                    CREATE TABLE IF NOT EXISTS SuperUsers (
                        guild_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                    
                        PRIMARY KEY (guild_id, user_id),
                    
                        FOREIGN KEY (guild_id)
                            REFERENCES GuildSettings(guild_id)
                            ON DELETE CASCADE
                    );
                ''')

                await temp_conn.execute('''
                    CREATE TABLE IF NOT EXISTS Birthdays (
                        guild_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        birthday TEXT NOT NULL,
                        last_congrats TEXT,
                    
                        PRIMARY KEY (guild_id, user_id),
                    
                        FOREIGN KEY (guild_id)
                            REFERENCES GuildSettings(guild_id)
                            ON DELETE CASCADE
                    );
                ''')

                await temp_conn.execute('''
                    CREATE TABLE IF NOT EXISTS SpamInfo (
                        guild_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        user_warning_count INTEGER NOT NULL DEFAULT 0,
                    
                        PRIMARY KEY (guild_id, user_id),
                    
                        FOREIGN KEY (guild_id)
                            REFERENCES GuildSettings(guild_id)
                            ON DELETE CASCADE
                    );
                ''')

                await temp_conn.execute('''
                    CREATE TABLE IF NOT EXISTS HiddenRoles (
                        guild_id INTEGER NOT NULL,
                        role_id INTEGER NOT NULL,
                    
                        PRIMARY KEY (guild_id, role_id),
                    
                        FOREIGN KEY (guild_id)
                            REFERENCES GuildSettings(guild_id)
                            ON DELETE CASCADE
                    );
                ''')

                await temp_conn.commit()
            except Exception as e:
                await self.logger.error(DM.get('failure_create_table_msg'), exc=e)
            finally:
                await temp_conn.close()

    @asynccontextmanager
    async def connect(self):
        async with self._write_lock:
            conn = await aiosqlite.connect(self.path)
            await conn.execute("PRAGMA foreign_keys = ON")
            try:
                yield conn
                await conn.commit()
            finally:
                await conn.close()
