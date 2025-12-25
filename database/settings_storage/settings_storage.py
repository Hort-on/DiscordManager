class SettingsStorage:
    def __init__(self, bot, db):
        self.db = db
        self.bot = bot
        self.guilds_settings = {}

    async def load_all(self):
        result = await self.db.get_data(

        )


    async def get_guild_settings(self, guild):
