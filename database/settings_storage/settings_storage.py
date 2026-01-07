from services.factories import DBScenarioFactory


class SettingsStorage:
    def __init__(self, bot, db_factory: DBScenarioFactory):
        self.db_factory = db_factory
        self.bot = bot

        self.guild_settings: dict[int, dict[str, object]] = {}
        self.guild_channels: dict[int, dict[str, object]] = {}
        self.guild_channels_to_send: dict[int, dict[int, int]] = {}
        self.guild_superusers: dict[int, set[int]] = {}
        self.guild_hidden_roles: dict[int, set[int]] = {}

    async def load_all_settings(self) -> None:
        for guild in self.bot.guilds:
            # --------------------------- load general guilds settings --------------------------- #
            setting_scenario = self.db_factory.for_fetch_all(guild.id, 'settings')
            result = await setting_scenario.db_proceed()

            self.guild_settings[guild.id] = result[0]

            # ------------------------------- load guild channels -------------------------------- #
            channel_scenario = self.db_factory.for_fetch_all(guild.id, 'guild_channels')
            channels = await channel_scenario.db_proceed()

            if channels:
                self.guild_channels[guild.id] = channels[0]

            # --------------------------- load guild channels to send ----------------------------- #
            channel_to_send_scenario = self.db_factory.for_fetch_all(guild.id, 'channels_to_send')
            channels_to_send = await channel_to_send_scenario.db_proceed()

            if channels_to_send:
                self.guild_channels_to_send[guild.id] = channels_to_send[0]

            # ------------------------------ load guilds superusers ------------------------------- #
            superuser_scenario = self.db_factory.for_fetch_all(guild.id, 'super_users')
            superusers = await superuser_scenario.db_proceed()

            if superusers:
                self.guild_superusers[guild.id] = {
                    user['user_id'] for user in superusers
                }

            # -------------------------------- load guilds roles ---------------------------------- #
            role_scenario = self.db_factory.for_fetch_all(guild.id, 'roles')
            hidden_roles = await role_scenario.db_proceed()

            if hidden_roles:
                self.guild_hidden_roles[guild.id] = {
                    row['role_id'] for row in hidden_roles
                }

    def get_guild_settings(self, guild_id: int) -> dict[str, object]:
        return self.guild_settings.get(guild_id, {})

    def get_guild_channels(self, guild_id: int) -> set[int]:
        return self.guild_channels.get(guild_id, set())

    def get_guild_channels_to_send(self, guild_id: int) -> dict[int, int]:
        return self.guild_channels_to_send.get(guild_id, {})

    def get_guild_superusers(self, guild_id: int) -> set[int]:
        return self.guild_superusers.get(guild_id, set())

    def get_hidden_roles(self, guild_id: int) -> set[int]:
        return self.guild_hidden_roles.get(guild_id, set())

    def update_guild_setting(self, guild_id: int, key: str, value) -> None:
        self.guild_settings.setdefault(guild_id, {})[key] = value
