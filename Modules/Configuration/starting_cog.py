from discord.ext import commands

from Modules.Configuration.starting_configuration import ConfigurationView
from db.data_base_setup import DB


class StartCog(commands.Cog):
    def __init__(self):
        self.db = DB()

    @commands.command(name='start')
    async def start_config(self, ctx):
        config_done = self.db.get_data(
            ctx.guild.id,
            'settings',
            'configuration_done'
        )

        if config_done:
            await ctx.send('```You have already configured the bot for this server.```',
                           delete_after=120
                           )
            return

        view = ConfigurationView()
        await ctx.send('```Welcome to the configuration!```',
                       view=view,
                       delete_after=60
                       )

async def setup(bot):
    await bot.add_cog(StartCog())
