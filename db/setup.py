import aiosqlite
from contextlib import asynccontextmanager

class DB:
    def __init__(self, path="database.sqlite"):
        self.path = path

        self.table_map = {
            "settings": "GuildSettings",
            "super_users": "SuperUsers",
            "channels": "SelectedChannels"
        }

    @asynccontextmanager
    async def connect(self):
        conn = await aiosqlite.connect(self.path)
        try:
            yield conn
            await conn.commit()
        finally:
            await conn.close()

    async def create_all_tables(self):
        async with self.connect() as db:
            await db.execute('''
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

            await db.execute('''
                CREATE TABLE IF NOT EXISTS SuperUsers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    UNIQUE(guild_id, user_id)
                )
            ''')

            await db.execute('''
                CREATE TABLE IF NOT EXISTS SelectedChannels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    channel_id INTEGER NOT NULL,
                    UNIQUE (guild_id, user_id)
                )
            ''')

    async def write_data(self, guild_id: int, name: str, data: dict) -> bool:
        table = self.table_map.get(name)
        if not table:
            raise ValueError('Unknown table name')

        async with self.connect() as db:
            try:
                async with db.execute(f"SELECT 1 FROM {table} WHERE guild_id=?", (guild_id,)) as cursor:
                    exists = await cursor.fetchone()

                if exists:
                    set_clause = ", ".join(f"{k}=?" for k in data.keys())
                    params = list(data.values()) + [guild_id]
                    await db.execute(f"UPDATE {table} SET {set_clause} WHERE guild_id=?", params)
                else:
                    columns = ["guild_id", *data.keys()]
                    placeholders = ["?"] * len(columns)
                    params = [guild_id] + list(data.values())
                    await db.execute(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})",
                                     params)

                await db.commit()
                return True
            except Exception as e:
                print(f"Error writing to DB: {e}")
                return False

    async def get_data(self, guild_id: int, name: str, *columns: str, fetch_all=False):
        table = self.table_map.get(name)
        if not table:
            raise ValueError("Unknown table name")

        columns_sql = ", ".join(columns) if columns else "*"
        async with self.connect() as db:
            if fetch_all:
                async with db.execute(f"SELECT {columns_sql} FROM {table} WHERE guild_id = ?", (guild_id,)) as cursor:
                    rows = await cursor.fetchall()
                    col_names = [desc[0] for desc in cursor.description]
                    return [dict(zip(col_names, row)) for row in rows]
            else:
                async with db.execute(f"SELECT {columns_sql} FROM {table} WHERE guild_id = ?", (guild_id,)) as cursor:
                    row = await cursor.fetchone()
                    if row is None:
                        return None
                    col_names = [desc[0] for desc in cursor.description]
                    return dict(zip(col_names, row))
