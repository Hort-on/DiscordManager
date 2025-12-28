import asyncio
from datetime import timedelta

from database.settings_storage.settings_storage import SettingsStorage

from utils.messages import SYSTEM_MSGS as SM


#TODO: ÏÈÒÀÍÍß ÙÎÄÎ ÁÅÇÏÅÊÈ
class UserManager:
    def __init__(self, settings: SettingsStorage):
        self.settings = settings

    @staticmethod
    async def block_user(
            message,
            duration_in_minutes,
            reason,
            is_games_violation #TODO: ìîæëèâî ïåğåğîáèòè
    ):

        user = message.author

        await user.timeout(timedelta(minutes=duration_in_minutes), reason=reason)

        await message.delete()

        notification = SM.get('user_blocked_msg').format(
            user=user.name,
            duration_in_minutes=duration_in_minutes,
            reason=reason
        )

        if not is_games_violation:
            await message.channel.send(
                notification + 'The user`s previous messages will be deleted```',
                delete_after=60)
            await UserManager.delete_user_message(message, user.id)
            return

        await message.channel.send(notification)

    @staticmethod
    async def delete_user_message(message, user_id):
        async for msg in message.channel.history(limit=20, oldest_first=False):
            if msg.author.id == user_id:
                await msg.delete()
                await asyncio.sleep(0.8)
