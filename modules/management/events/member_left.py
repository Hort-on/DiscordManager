from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

from services.utils.messages import GENERAL_MSGS as GM


class MemberLeftNotification:
    def __init__(self, bot, settings: SettingsStorage):
        self.bot = bot
        self.settings = settings

    async def check_if_notification(self, member):
        if not self.settings.dict_storage.get_dict(
                StorageTarget.SETTINGS,
                member.guild.id,
                'member_left'
        ):
            return

        await self.process_guild_channel(member)

    async def process_guild_channel(self, member):
        channel_id = self.settings.dict_storage.get_dict(
            StorageTarget.SETTINGS,
            member.guild.id,
            'notification_channel_id'
        )

        if not channel_id:
            return

        await self.send_notification_message(channel_id, member)

    async def send_notification_message(self, channel_id, member):
        channel = await self.bot.get_channel(channel_id)

        if not channel:
            return

        await channel.send(GM.get('user_left_msg').format(member=member.name))
