from discord.ext import tasks

from database.data_base_model import DB
from modules.Logging.logging import Logger
from modules.Management.events_processing.member_left_event import MemberLeftNotification
from modules.Management.message_processing.BadWordsHandler import BadWordsHandler
from modules.birthdays.birthday import Birthday
from utils.bad_words import invitation_pattern


class BotController:
    def __init__(self, bot):
        self.bot = bot
        self.db = DB()

        self.logger = Logger()
        self.birthday = Birthday()
        self.bad_words = BadWordsHandler()
        self.member_left = MemberLeftNotification(self.bot, self.db)

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

            if len(message.content) > 5 and is_caps(message.content):
                await message.delete()
                await message.channel.send(f"```{nick}, please stop using the caps.```")
                return

            await handle_spam(message)

        await self.handle_message(message)
        await self.bot.process_commands(message)

    async def on_raw_reaction_add(self, payload):
        result = await self.db.get_data(
            payload.guild_id,
            'settings',
            'verification',
            'verification_channel_id',
            'verification_msg_id'
        )

        if not result or not all(result.values()):
            return

        if payload.channel_id != result.get('verification_channel_id'):
            return

        if payload.message_id != result.get('verification_msg_id'):
            return

        # тут твоя логіка

    async def on_member_remove(self, member):
        await self.member_left.check_if_notification(member)


    # --------------------------- LOOPS ---------------------------

    @tasks.loop(hours=24)
    async def daily_birthday_check(self):
        for guild in self.bot.guilds:
            await self.birthday.check_birthday(guild.id)

    # --------------------------- MESSAGE HANDLING ---------------------------

    async def handle_message(self, message):
        cleaned = self.bad_words.prepare(message.content)
        await self.bad_words.check(message, cleaned)
