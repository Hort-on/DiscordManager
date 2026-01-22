from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

from services.utils.messages import GENERAL_MSGS as GM


class MemberLeftNotification:
    def __init__(self, bot, settings: SettingsStorage):
        self.bot = bot
        self.settings = settings

    async def check_if_notification(self, member):
        notify = self.settings.dict_storage.for_dict_get(
            'member_left',
            target=StorageTarget.SETTINGS,
            guild_id=member.guild.id
        )

        if not notify.get('member_left'):
            return

        await self.process_guild_channel(member=member)

    async def process_guild_channel(self, member):
        channel_id = self.settings.dict_storage.for_dict_get(
            'notification_channel_id',
            target=StorageTarget.SETTINGS,
            guild_id=member.guild.id,
        )

        if not channel_id.get('notification_channel_id'):
            return

        await self.send_notification_message(channel_id=channel_id, member=member)

    async def send_notification_message(self, channel_id, member):
        channel = self.bot.get_channel(channel_id)

        if not channel:
            return

        await channel.send(GM.get('user_left_msg').format(member=member.name))
