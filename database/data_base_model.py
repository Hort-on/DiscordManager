import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

import aiosqlite

from general_services.logger.logger import Logger


class DB:
    def __init__(self, logger: Logger, path: Path):
        self.logger = logger
        self.path = str(path)
        self._write_lock = asyncio.Lock()

    async def init_tables(self):
        temp_conn = await aiosqlite.connect(self.path)
        await temp_conn.execute("PRAGMA synchronous = NORMAL")
        await temp_conn.execute("PRAGMA journal_mode = WAL")
        await temp_conn.execute("PRAGMA foreign_keys = ON")
        try:
            await temp_conn.execute("""
                CREATE TABLE IF NOT EXISTS GuildSettings (
                    guild_id INTEGER PRIMARY KEY,
                    language TEXT NOT NULL DEFAULT 'en',
                    birthday INTEGER NOT NULL DEFAULT 0,
                    congrats INTEGER NOT NULL DEFAULT 0,
                
                    verification INTEGER NOT NULL DEFAULT 0,
                    verification_role_id INTEGER DEFAULT NULL,
                    verification_message_id INTEGER DEFAULT NULL,
                    
                    invitation_blocking INTEGER NOT NULL DEFAULT 0,
                    spam_checking INTEGER NOT NULL DEFAULT 0,
                    flood_checking INTEGER NOT NULL DEFAULT 0,
                    caps_checking INTEGER NOT NULL DEFAULT 0,
                
                    send_messages INTEGER NOT NULL DEFAULT 1,
                    member_left INTEGER NOT NULL DEFAULT 0,
                    block_users INTEGER NOT NULL DEFAULT 0,
                    write_audit_log INTEGER NOT NULL DEFAULT 1,
                    role_manager INTEGER NOT NULL DEFAULT 0,
                    anti_bot INTEGER NOT NULL DEFAULT 0
                );
            """)

            await temp_conn.execute("""
                CREATE TABLE IF NOT EXISTS SystemChannels (
                    guild_id INTEGER PRIMARY KEY,
                    
                    congrats_channel_id INTEGER DEFAULT NULL,
                    verification_channel_id INTEGER DEFAULT NULL,
                    notification_channel_id INTEGER DEFAULT NULL,
                    
                    FOREIGN KEY (guild_id)
                        REFERENCES GuildSettings(guild_id)
                        ON DELETE CASCADE
                );
            """)

            await temp_conn.execute("""
                CREATE TABLE IF NOT EXISTS ChannelsToSend (
                    guild_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    channel_id INTEGER NOT NULL,

                    PRIMARY KEY (guild_id, user_id),

                    FOREIGN KEY (guild_id)
                        REFERENCES GuildSettings(guild_id)
                        ON DELETE CASCADE
                );
            """)

            await temp_conn.execute("""
                CREATE TABLE IF NOT EXISTS SuperUsers (
                    guild_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                
                    PRIMARY KEY (guild_id, user_id),
                
                    FOREIGN KEY (guild_id)
                        REFERENCES GuildSettings(guild_id)
                        ON DELETE CASCADE
                );
            """)

            await temp_conn.execute("""
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
            """)

            await temp_conn.execute("""
                CREATE TABLE IF NOT EXISTS HiddenRoles (
                    guild_id INTEGER NOT NULL,
                    role_id INTEGER NOT NULL,
                
                    PRIMARY KEY (guild_id, role_id),
                
                    FOREIGN KEY (guild_id)
                        REFERENCES GuildSettings(guild_id)
                        ON DELETE CASCADE
                );
            """)

            await temp_conn.execute("""
                CREATE TABLE IF NOT EXISTS HiddenChannels (
                    guild_id INTEGER NOT NULL,
                    channel_id INTEGER NOT NULL,

                    PRIMARY KEY (guild_id, channel_id),

                    FOREIGN KEY (guild_id)
                        REFERENCES GuildSettings(guild_id)
                        ON DELETE CASCADE
                );
            """)

            await temp_conn.execute("""
                CREATE TABLE IF NOT EXISTS TempChannels (
                    guild_id INTEGER NOT NULL,
                    channel_id INTEGER NOT NULL,
                    owner_id INTEGER,

                    PRIMARY KEY (guild_id, channel_id),

                    FOREIGN KEY (guild_id)
                        REFERENCES GuildSettings(guild_id)
                        ON DELETE CASCADE
                );
            """)

            async with temp_conn.execute("PRAGMA table_info(TempChannels)") as cursor:
                columns = {row[1] for row in await cursor.fetchall()}

            if "owner_id" not in columns:
                await temp_conn.execute(
                    "ALTER TABLE TempChannels ADD COLUMN owner_id INTEGER"
                )

            await temp_conn.execute("""
                CREATE TABLE IF NOT EXISTS Groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER NOT NULL,
                    owner_id INTEGER NOT NULL,
                    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
                    
                    UNIQUE(guild_id, owner_id),
                    
                    FOREIGN KEY (guild_id)
                        REFERENCES GuildSettings(guild_id)
                        ON DELETE CASCADE
                );
            """)

            await temp_conn.execute("""
                CREATE TABLE IF NOT EXISTS GroupMembers (
                    group_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                
                    PRIMARY KEY (group_id, user_id),
                
                    FOREIGN KEY (group_id)
                        REFERENCES Groups(id)
                        ON DELETE CASCADE
                );
            """)

            await temp_conn.commit()
        except Exception as e:
            await self.logger.error("Не вдалося створити таблицю", exc=e)
        finally:
            await temp_conn.close()

    @asynccontextmanager
    async def connect_read(self):
        conn = await aiosqlite.connect(self.path)
        await conn.execute("PRAGMA synchronous = NORMAL")
        await conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
        finally:
            await conn.close()

    @asynccontextmanager
    async def connect_write(self):
        async with self._write_lock:
            conn = await aiosqlite.connect(self.path)
            await conn.execute("PRAGMA synchronous = NORMAL")
            await conn.execute("PRAGMA foreign_keys = ON")
            try:
                yield conn
                await conn.commit()
            finally:
                await conn.close()
