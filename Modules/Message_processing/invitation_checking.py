from Modules.Logging.logging import Logger
from config import SUPERUSERS


async def invitation_check(nick, message):
    if message.author.id not in SUPERUSERS:
        await message.delete()
        await message.channel.send(
            f'```{nick}, advertising other servers without the administration\'s permission is prohibited on this server.```',
            delete_after=60)
        await logger("BOT", f'The user: {nick}, sent an invitation: {message.content}',
                     'Logs/invitations.log')
    else:
        return
