import discord
from discord.ext import tasks

from database.data_base_model import DB
from database.settings_storage.settings_storage import SettingsStorage

from services.factories.db_factory.db_scenario_factory import DBScenarioFactory
from services.utils.bad_words import invitation_pattern

from modules.logger.logger import Logger
from modules.management.events_processing.member_left_event import MemberLeftNotification
from modules.management.message_processing.BadWordsHandler import BadWordsHandler
from modules.birthdays.birthday_repo import BirthdayManager


class BotController:
    def __init__(
            self,
            bot,
            db_connect: DB,
            db_factory: DBScenarioFactory,
            logger: Logger,
            settings: SettingsStorage,
            birthday_manager: BirthdayManager,
            bad_words_handler: BadWordsHandler,
            member_left_notify: MemberLeftNotification

    ):
        self.bot = bot

        self.db_connect = db_connect
        self.db_factory = db_factory

        self.logger = logger

        self.settings = settings
        self.birthday_manager = birthday_manager
        self.bad_words = bad_words_handler
        self.member_left_notify = member_left_notify

        self.bot.add_listener(self.on_ready)
        self.bot.add_listener(self.on_message)
        self.bot.add_listener(self.on_raw_reaction_add)
        self.bot.add_listener(self.on_member_remove)
        self.bot.add_listener(self.on_guild_remove)
        self.bot.add_listener(self.on_guild_join)

    # --------------------------- EVENTS --------------------------- #

    async def on_ready(self):
        print(f"Connected as {self.bot.user}")

        if not self.daily_birthday_check.is_running():
            self.daily_birthday_check.start()

        await self.settings.load_all_settings()

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
        result = await self.db.get_data(  # TODO: переробити
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
        await self.member_left_notify.check_if_notification(member)

    async def on_guild_remove(self, guild: discord.Guild):
        delete_guild_scenario = self.db_factory.for_remove_guild(guild.id)
        await delete_guild_scenario.db_proceed()

    async def on_guild_join(self, guild: discord.Guild):
        scenario = self.db_factory.for_init_guild(guild.id)
        await scenario.db_proceed()

    # --------------------------- LOOPS ---------------------------

    @tasks.loop(hours=24)
    async def daily_birthday_check(self):
        await self.birthday_repo.check_daily_birthday()

    # --------------------------- MESSAGE HANDLING ---------------------------

    async def handle_message(self, message):
        ...
