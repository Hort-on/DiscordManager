class MemberLeftNotification:
    def __init__(self, bot, db):
        self.db = db
        self.bot = bot

    async def check_if_notification(self, member):
        result = await self.db.get_data(
            member.guild.id,
            'settings',
            'member_left'
        )

        if not result.get('member_left'):
            return

        await self.process_guild_channel(member)

    async def process_guild_channel(self, member):
        channel_id = await self.db.get_data(
            member.guild.id,
            'settings',
            'system_channel_id'
        )

        if not channel_id:
            return

        await self.send_notification_message(channel_id, member)

    async def send_notification_message(self, channel, member):
        channel = await self.bot.get_channel(channel)

        if not channel:
            return

        await channel.send(f"User: {member.displayname} has left the server.")
