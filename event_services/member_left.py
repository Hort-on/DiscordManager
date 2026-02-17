from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

from general_services.utils.messages import GENERAL_MSGS as GM


class MemberLeftNotification:
    def __init__(self, bot, settings: SettingsStorage):
        self.bot = bot
        self.settings = settings

    async def check_if_notification(self, member):
        result = self.settings.dict_storage.for_dict_get(
            'member_left',
            target=StorageTarget.SETTINGS,
            guild_id=member.guild.id
        )

        channel = self.settings.dict_storage.for_dict_get(
            'sys_channels',
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=member.guild.id
        )

        if not result.get('member_left') and channel.get('notification_channel_id'):
            return

        await self.send_notification(member=member)

    async def send_notification(self, member):
        channel_id = self.settings.dict_storage.for_dict_get(
            'notification_channel_id',
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=member.guild.id,
        )

        channel = self.bot.get_channel(channel_id)

        if not channel:
            return

        await channel.send(GM.get('user_left_msg').format(member=member.name))
