from modules.logger.logger import Logger


class SettingsStorage:
    def __init__(self, bot, db, logger: Logger):
        self.db = db
        self.bot = bot
        self.logger = logger
        self.guilds_settings = {}
        self.guilds_superusers = {}
        self.guilds_roles = {}

    async def load_all_settings(self) -> None:
        for guild in self.bot.guilds:
            guild_data_scenario = self.db.for_fetch_all(
                guild.id,
                'settings'
            )

            result = await guild_data_scenario.db_proceed()
            if not result:
                continue

            self.guilds_settings[guild.id] = result

        for guild in self.bot.guilds:
            superusers_scenario = self.db.for_get_data(
                guild.id,
                'super_users',
                self.logger,
                'userId'
            )

            result = await superusers_scenario.db_proceed()
            if not result:
                continue

            self.guilds_superusers[guild.id] = result

    def get_guild_settings(self, guild_id: int) -> dict:
        return self.guilds_superusers.get(guild_id, {})

    def get_guild_superusers(self, guild_id: int) -> dict:
        return self.guilds_superusers.get(guild_id, {})

    def get_guild_roles(self, guild_id: int) -> dict:
        return self.guilds_roles.get(guild_id, {})

    def update_guild_setting(self, guild_id: int, key: str, value) -> None:
        self.guilds_settings.setdefault(guild_id, {})[key] = value
