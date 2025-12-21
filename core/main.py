from discord.ext import tasks

from modules.Logging.logging import Logger
from modules.birthdays.birthday import Birthday
from modules.Message_processing.bad_games_handling import handle_bad_games
from utils import bad_words
from utils.bad_words import invitation_pattern, blacklist_word_pattern, \
    blacklist_games_pattern
from modules.Message_processing.BadWordsHandler import BadWordsHandler
from modules.Message_processing.caps_checking import is_caps
from modules.Message_processing.invitation_checking import invitation_check
from modules.Message_processing.spam_handling import handle_spam
from bot import bot


class BotController:
    def __init__(self):
        self.bot = bot

        self.logger = Logger()
        self.birthday = Birthday()
        self.bad_words = BadWordsHandler()

        self.bot.add_listener(self.on_ready)
        self.bot.add_listener(self.on_message)
        self.bot.add_listener(self.on_raw_reaction_add)
        self.bot.add_listener(self.on_member_remove)

    # --------------------------- EVENTS --------------------------- #

    async def on_ready(self):
        print(f"Connected as {self.bot.user}")

        if not self.daily_birthday_check.is_running():
            self.daily_birthday_check.start()

    async def on_message(self, message):
        # TODO: потрібно зробити перевірку суперюзерів з бд
        # TODO: потрібно переписати on_message, зробити більш простим та читабельним
        if message.guild is None and message.author.id in SUPERUSERS:
            if hasattr(self.bot, 'selected_channel') and self.bot.selected_channel:
                await self.bot.selected_channel.send(message.content)
            else:
                await message.author.send('```First select the channel for sending messages.```')
            return

        if message.author.bot:
            return

        if message.guild:
            nick = message.author.nick if message.author.nick else message.author.name

            if invitation_pattern.search(message.content):
                await invitation_check(nick, message)

            cleaned_message = bad_words.remove_punctuation(message.content.lower())
            original_message = cleaned_message
            cleaned_message = bad_words.replace_similar_chars(cleaned_message)

            if blacklist_word_pattern.search(cleaned_message):
                await bad_words.check_for_bad_words(message, nick)
            elif blacklist_word_pattern.search(original_message):
                await bad_words.check_for_bad_words(message, nick)

            if blacklist_games_pattern.search(cleaned_message):
                await handle_bad_games(message, nick)
            elif blacklist_games_pattern.search(original_message):
                await handle_bad_games(message, nick)

            if len(message.content) > 4 and is_caps(message.content):
                await message.delete()
                await message.channel.send(f"```{nick}, please stop using the caps.```")
                return

            await handle_spam(message)

        await self.handle_message(message)
        await self.bot.process_commands(message)

    async def on_raw_reaction_add(self, payload):
        if payload.user_id == bot.user.id:
            return

        # TODO: потрібно витягувати id повідомлень та каналів з бд для конкретної гільдії

        ukr_message_id = 0
        eng_message_id = 0
        channel_id = 0

        if payload.channel_id == channel_id:
            channel = self.bot.get_channel(payload.channel_id)

            # logs events if enabled
            if channel is None:
                await logger.error(f"Channel with ID {payload.channel_id} not found.")
                return

            guild = self.bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)

            # logs events if enabled
            if user is None:
                await logger.error(f"User with ID {payload.user_id} not found.")
                return

            message = await channel.fetch_message(payload.message_id)
            handler = VerificationHandler()

            # checks the ID of the message to which the reaction was added
            if payload.message_id == eng_message_id:
                user_eu = False
            elif payload.message_id == ukr_message_id:
                user_eu = True
            else:
                return

            await handler.handle_verification_reaction(guild, user, user_eu, message, payload.emoji)

    async def on_member_remove(self, member):
        # TODO: потрібно витягувати канал з бд для конкретної гільдії
        channel_id = 0
        channel = bot.get_channel(int(channel_id))

        if channel is not None:
            await channel.send(f"User: {member} has left the server.")
        else:
            await logger.error(f"Channel with the ID {channel} not found.")
            return

    # --------------------------- LOOPS ---------------------------

    @tasks.loop(hours=24)
    async def daily_birthday_check(self):
        for guild in self.bot.guilds:
            await self.birthday.check_birthday(guild.id)

    # --------------------------- MESSAGE HANDLING ---------------------------

    async def handle_message(self, message):
        cleaned = self.bad_words.prepare(message.content)
        await self.bad_words.check(message, cleaned)
