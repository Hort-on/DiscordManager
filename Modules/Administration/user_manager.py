import asyncio
from datetime import timedelta

from db.setup import DB


# охрюммъ ындн аегоейх
class UserManager:
    def __init__(self):
        self.db = DB()



    @staticmethod
    async def block_user(message, duration_in_minutes, reason, is_games_violation=False):
        user = message.author

        # Blocks the user
        await user.timeout(timedelta(minutes=duration_in_minutes), reason=reason)

        await message.delete()

        # The message that will be sent in the channel where the violation occurred
        notification = f'```{user.nick} has been blocked for {duration_in_minutes} minutes because of: {reason}.'

        if is_games_violation:
            await message.channel.send(notification)
        else:
            await message.channel.send(
                notification + 'The user`s previous messages will be deleted```',
                delete_after=60)
            await UserManager.delete_user_message(message, user.id)

    @staticmethod
    async def delete_user_message(message, user_id):
        async for msg in message.channel.history(limit=20, oldest_first=False):
            if msg.author.id == user_id:
                await msg.delete()
                await asyncio.sleep(0.8)
