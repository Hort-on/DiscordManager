from discord.ext import commands

from modules.Management.management import Management
from database.data_base_model import DB


class ManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DB()

    @commands.command(name='mg')
    async def management(self, ctx):
        super_users_data = await self.db.get_data(
            ctx.guild.id,
            'super_users',
            'user_id'
        )

        if not super_users_data:
            await ctx.send(
                '```Only superusers are allowed to use this command!'
                'Super users are not configured for this server!'
                'To set superusers, please type "!mg"'
                ' and press the button "management" -> "set superusers".```',
                delete_after=120
            )
            return

        super_users = [user.get('user_id') for user in super_users_data]

        if ctx.author.id not in super_users:
            await ctx.send('```You do not have permission to use this feature!```',
                           delete_after=120)
            return

        settings = await self.db.get_data(
            ctx.guild.id,
            "settings",
            'birthday',
            'sending_messages',
            'deleting_message',
            'congrats_channel_id',
            'system_channel_id',
            'verification_channel_id',
            'configuration_done'
        )

        if not settings.get('configuration_done'):
            await ctx.send('```Settings are not configured for this server yet!```', delete_after=120)
            return

        view = Management(ctx, self.bot, settings)
        await ctx.send("Select an action:", view=view, delete_after=60)


async def setup(bot):
    await bot.add_cog(ManagementCog(bot))

