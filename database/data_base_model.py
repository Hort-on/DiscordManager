import aiosqlite
from contextlib import asynccontextmanager

class DB:
    def __init__(self, path='database.sqlite'):
        self.path = path
        self._create_all_tables()

        self.table_map = {
            'settings': "GuildSettings",
            'super_users': "SuperUsers",
            'channels': "SelectedChannels",
            'birthdays': "birthdays"
        }

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

                    system_channel_id INTEGER DEFAULT NULL,

                    verification BOOLEAN DEFAULT TRUE NOT NULL,
                    verification_channel_id INTEGER DEFAULT NULL,
                    verification_msg_id INTEGER DEFAULT NULL,

                    block_users BOOLEAN DEFAULT TRUE NOT NULL,
                    message_management BOOLEAN DEFAULT TRUE NOT NULL,
                    invitation_checking BOOLEAN DEFAULT TRUE NOT NULL,
                    spam_checking BOOLEAN DEFAULT TRUE NOT NULL,
                    member_left BOOLEAN DEFAULT TRUE NOT NULL,
                    set_permissions BOOLEAN DEFAULT TRUE NOT NULL,
                    sending_messages BOOLEAN DEFAULT TRUE NOT NULL,
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

    async def write_data(self, guild_id: int, table_name: str, data: dict) -> bool:
        table = self.table_map.get(table_name)
        if not table:
            raise ValueError('Unknown table name')

        async with self.connect() as db:
            try:
                columns = ", ".join(["guild_id", *data.keys()])
                placeholders = ", ".join(["?"] * (len(data) + 1))
                update_clause = ", ".join(f"{k}=excluded.{k}" for k in data.keys())

                await db.execute(
                    f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) "
                    f"ON CONFLICT(guild_id) DO UPDATE SET {update_clause}",
                    (guild_id, *data.values())
                )
                await db.commit()
                return True
            except Exception as e:
                print(f"Error writing to DB: {e}")
                return False

    async def get_data(self, guild_id: int, table_name: str, *columns: str, fetch_all=False):
        table = self.table_map.get(table_name)
        if not table:
            raise ValueError("Unknown table name")

        columns_sql = ", ".join(columns) if columns else "*"
        query = f"SELECT {columns_sql} FROM {table} WHERE guild_id = ?"

        async with self.connect() as db:
            async with db.execute(query, (guild_id,)) as cursor:
                col_names = [desc[0] for desc in cursor.description]

                if fetch_all:
                    rows = await cursor.fetchall()
                    return [dict(zip(col_names, row)) for row in rows]
                else:
                    row = await cursor.fetchone()
                    return dict(zip(col_names, row)) if row else None
