import discord

from core.bot import bot

from services.utils.messages import CONFIG_MSGS as CM


class VerificationHandler:
    def __init__(self):
        self.bot = bot
        self.vrf_mg = CM  #TODO: розібратись з vrf_msg що це має бути
        #TODO: витягувати id ролей з бд
        #TODO: переробити цей файл

    async def verification_process(self):

    async def send_user_message(self, user, msg_key):
        """Sends a message to the user if enabled"""
        try:
            await user.send(self.vrf_mg[msg_key])
        except discord.Forbidden:
            print(f"Impossible to send the message to: {user.name}. probably the user has restricted DM.")

    async def handle_accept_reaction(self, guild, user, user_eu):
        """Handles the accept (✅) reaction"""
        role = guild.get_role(self.accepted_role_id)
        if not role:
            await self.logger.error(f'The role with ID {self.accepted_role_id} not found.')
            return

        await user.add_roles(role)

        declined_role = guild.get_role(self.declined_role_id)
        if declined_role in user.roles:
            await user.remove_roles(declined_role)

        msg_key = 'eng_accept' if user_eu else 'ukr_accept'
        await self.send_user_message(user, msg_key)

        await self.logger.verification(f'The user: {user} has accepted the rules.')

    async def handle_decline_reaction(self, guild, user, user_eu):
        """Handles the decline (❌) reaction"""
        role = guild.get_role(self.declined_role_id)
        if not role:
            await self.logger.error(f'The role with ID {self.declined_role_id} not found.')
            return

        roles_to_remove = [r for r in user.roles if r.id != guild.id]
        if roles_to_remove:
            await user.remove_roles(*roles_to_remove)

        await user.add_roles(role)

        msg_key = 'eng_decline' if user_eu else 'ukr_decline'
        await self.send_user_message(user, msg_key)

        await self.logger.verification(f'The user: {user} has declined the server`s rules') # TODO: це має записувати бот в логи або відправляти повідомлення у системний канал

        channel = self.bot.get_channel(self.mc)
        await channel.send(f'```The user: {user} has declined the server`s rules```')

    async def handle_verification_reaction(self, guild, user, user_eu, message, emoji):
        """Main method to handle verification reactions"""
        match str(emoji):
            case '✅':
                await self.handle_accept_reaction(guild, user, user_eu)

            case '❌':
                await self.handle_decline_reaction(guild, user, user_eu)

            case _:
                await self.logger.error(f"Unsupported emoji: {emoji}")

        await message.remove_reaction(emoji, user)
