from database.data_base_model import DB

from services.logger.logger import Logger
from services.utils.messages import DB_MSGS as DM


class DataBaseScenario:
    table_map = {
        'settings': "GuildSettings",
        'guild_channels': "GuildSelectedChannels",
        'hidden_channels': "HiddenChannels",
        'channels_to_send': "ChannelsToSend",
        'super_users': "SuperUsers",
        'birthdays': "Birthdays",
        'spam_info': "SpamInfo",
        'roles': "HiddenRoles"
    }

    USER_TABLES = [
        'super_users',
        'channels',
        'birthdays',
        'spam_info'
    ]

    def __init__(
            self,
            db_connect: DB,
            logger: Logger,
            guild_id: int | None
    ):
        self.logger = logger
        self.db_connect = db_connect
        self.guild_id = guild_id

    async def db_proceed(self):
        try:
            return await self._execute()
        except Exception as e:
            await self.logger.error(
                await self.logger.error(DM.get('failure_read_msg'), exc=e)
            )
            return None

    async def _execute(self):
        raise NotImplementedError

    def _get_table(self, table_name: str) -> str:
        table = self.table_map.get(table_name)
        if not table:
            raise ValueError(f'Unknown table name: {table_name}')
        return table
