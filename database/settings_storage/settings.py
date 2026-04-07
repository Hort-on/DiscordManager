import asyncio

from database.db_factory.db_scenario_factory import DBFactory
from database.settings_storage.settings_manager import (
    DictStorageManager,
    SetStorageManager,
    StorageTarget,
)


class SettingsStorage:
    def __init__(self, bot, db_factory: DBFactory):
        self.db_factory = db_factory
        self.bot = bot

        self._guild_settings: dict[int, dict[str, int]] = {}
        self._guild_system_channels: dict[int, dict[str, int]] = {}
        self._guild_channels_to_send: dict[int, dict[int, int]] = {}

        self._guild_hidden_channels: dict[int, set[int]] = {}
        self._guild_hidden_roles: dict[int, set[int]] = {}
        self._guild_superusers: dict[int, set[int]] = {}

        self.set_storage: SetStorageManager = SetStorageManager(
            {
                StorageTarget.HIDDEN_CHANNELS: self._guild_hidden_channels,
                StorageTarget.SUPERUSERS: self._guild_superusers,
                StorageTarget.HIDDEN_ROLES: self._guild_hidden_roles,
            }
        )

        self.dict_storage: DictStorageManager = DictStorageManager(
            {
                StorageTarget.SETTINGS: self._guild_settings,
                StorageTarget.SYSTEM_CHANNELS: self._guild_system_channels,
                StorageTarget.CHANNELS_TO_SEND: self._guild_channels_to_send,
            }
        )

    async def load_all_guilds_settings(self) -> None:
        await asyncio.gather(
            *(self._load_guild_settings(guild.id) for guild in self.bot.guilds)
        )

    async def reload_guild(self, guild_id: int) -> None:
        await self._load_guild_settings(guild_id)

    async def _load_guild_settings(self, guild_id: int) -> None:
        db_init = self.db_factory.for_init_guild(guild_id=guild_id)
        await db_init.db_proceed()

        # --------------------------- load general guilds settings --------------------------- #
        settings_scenario = self.db_factory.for_fetch_all(
            guild_id=guild_id, table_name="settings"
        )
        result = await settings_scenario.db_proceed()

        if result:
            self._guild_settings[guild_id] = result[0]

        # ------------------------------- load system channels -------------------------------- #
        sys_channels = self.db_factory.for_fetch_all(
            guild_id=guild_id, table_name="sys_channels"
        )
        sys_ch = await sys_channels.db_proceed()

        if sys_ch:
            row = sys_ch[0]

            self._guild_system_channels[guild_id] = {
                k: v for k, v in row.items() if k != "guild_id"
            }

        # ---------------------------- load guild hidden channels ----------------------------- #
        hidden_channels = self.db_factory.for_fetch_all(
            guild_id=guild_id, table_name="hidden_channels"
        )

        hidden_ch = await hidden_channels.db_proceed()

        if hidden_ch:
            self._guild_hidden_channels[guild_id] = {
                row["channel_id"] for row in hidden_ch
            }

        # --------------------------- load guild channels to send ----------------------------- #
        channel_to_send_scenario = self.db_factory.for_fetch_all(
            guild_id=guild_id, table_name="channels_to_send"
        )
        channels_to_send = await channel_to_send_scenario.db_proceed()

        if channels_to_send:
            self._guild_channels_to_send[guild_id] = {
                row["user_id"]: row["channel_id"] for row in channels_to_send
            }

        # ------------------------------ load guilds superusers ------------------------------- #
        superuser_scenario = self.db_factory.for_fetch_all(
            guild_id=guild_id, table_name="super_users"
        )
        superusers = await superuser_scenario.db_proceed()

        self._guild_superusers[guild_id] = {user["user_id"] for user in superusers}

        # -------------------------------- load guilds roles ---------------------------------- #
        role_scenario = self.db_factory.for_fetch_all(
            guild_id=guild_id, table_name="roles"
        )
        hidden_roles = await role_scenario.db_proceed()

        if hidden_roles:
            self._guild_hidden_roles[guild_id] = {
                row["role_id"] for row in hidden_roles
            }
