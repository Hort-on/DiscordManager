import asyncio
from datetime import timedelta


#TODO: охрюммъ ындн аегоейх
class UserManager:
    @staticmethod
    async def block_user(message, duration_in_minutes, reason, is_games_violation=False):
        user = message.author

        await user.timeout(timedelta(minutes=duration_in_minutes), reason=reason)

        await message.delete()

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
