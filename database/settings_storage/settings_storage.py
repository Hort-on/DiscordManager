from database.db_factory.db_scenario_factory import DBScenarioFactory


class SettingsStorage:
    def __init__(self, bot, db_factory: DBScenarioFactory):
        self.db_factory = db_factory
        self.bot = bot

        self.guilds_settings: dict[int, dict[str, object]] = {}
        self.guilds_superusers: dict[int, set[int]] = {}
        self.guilds_roles: dict[int, dict] = {}

    async def load_all_settings(self) -> None:
        for guild in self.bot.guilds:
            scenario = self.db_factory.for_fetch_all(guild.id, 'settings')
            result = await scenario.db_proceed()
            if result:
                self.guilds_settings[guild.id] = result[0]

        for guild in self.bot.guilds:
            scenario = self.db_factory.for_fetch_all(guild.id, 'super_users')
            result = await scenario.db_proceed()
            if result:
                self.guilds_superusers[guild.id] = {
                    row["user_id"] for row in result
                }

    def get_guild_settings(self, guild_id: int) -> dict[str, object]:
        return self.guilds_settings.get(guild_id, {})

    def get_guild_superusers(self, guild_id: int) -> set[int]:
        return self.guilds_superusers.get(guild_id, set())

    def update_guild_setting(self, guild_id: int, key: str, value) -> None:
        self.guilds_settings.setdefault(guild_id, {})[key] = value
