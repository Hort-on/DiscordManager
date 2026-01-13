from database.settings_storage.settings_manager import SetStorageManager, StorageTarget, DictStorageManager

from services.factories.db_factory.db_scenario_factory import DBScenarioFactory


class SettingsStorage:
    def __init__(self, bot, db_factory: DBScenarioFactory):
        self.db_factory = db_factory
        self.bot = bot

        self._guild_settings: dict[int, dict[str, int]] = {}
        self._guild_selected_channels: dict[int, dict[str, int]] = {}
        self._guild_hidden_channels: dict[int, set[int]] = {}
        self._guild_channels_to_send: dict[int, dict[int, int]] = {}
        self._guild_superusers: dict[int, set[int]] = {}
        self._guild_hidden_roles: dict[int, set[int]] = {}

        self.set_storage = SetStorageManager({
            StorageTarget.HIDDEN_CHANNELS: self._guild_hidden_channels,
            StorageTarget.SUPERUSERS: self._guild_superusers,
            StorageTarget.HIDDEN_ROLES: self._guild_hidden_roles,
        })

        self.dict_storage = DictStorageManager({
            StorageTarget.SETTINGS: self._guild_settings,
            StorageTarget.SELECTED_CHANNELS: self._guild_selected_channels,
            StorageTarget.CHANNELS_TO_SEND: self._guild_channels_to_send
        })

    async def load_all_settings(self) -> None:
        for guild in self.bot.guilds:
            # --------------------------- load general guilds settings --------------------------- #
            setting_scenario = self.db_factory.for_fetch_all(guild.id, 'settings')
            result = await setting_scenario.db_proceed()

            if result:
                self._guild_settings[guild.id] = result[0]

            # ------------------------------- load guild channels -------------------------------- #
            channel_scenario = self.db_factory.for_fetch_all(guild.id, 'guild_channels')
            channels = await channel_scenario.db_proceed()

            if channels:
                self._guild_selected_channels[guild.id] = channels[0]

            # ---------------------------- load guild hidden channels ----------------------------- #
            channel_scenario = self.db_factory.for_fetch_all(guild.id, 'hidden_channels')
            channels = await channel_scenario.db_proceed()

            if channels:
                self._guild_hidden_channels[guild.id] = channels[0]

            # --------------------------- load guild channels to send ----------------------------- #
            channel_to_send_scenario = self.db_factory.for_fetch_all(guild.id, 'channels_to_send')
            channels_to_send = await channel_to_send_scenario.db_proceed()

            if channels_to_send:
                self._guild_channels_to_send[guild.id] = channels_to_send[0]

            # ------------------------------ load guilds superusers ------------------------------- #
            superuser_scenario = self.db_factory.for_fetch_all(guild.id, 'super_users')
            superusers = await superuser_scenario.db_proceed()

            if superusers:
                self._guild_superusers[guild.id] = {
                    user['user_id'] for user in superusers
                }

            # -------------------------------- load guilds roles ---------------------------------- #
            role_scenario = self.db_factory.for_fetch_all(guild.id, 'roles')
            hidden_roles = await role_scenario.db_proceed()

            if hidden_roles:
                self._guild_hidden_roles[guild.id] = {
                    row['role_id'] for row in hidden_roles
                }
