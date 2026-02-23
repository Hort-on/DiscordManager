from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from event_services.member_left import MemberLeftNotification

from features.auto_moderation.verification.flow import VerificationFlow
# from discord.ext import tasks
from general_services.other_services.ask_user_birthday import UserJoinBirthdayService
# from general_services.utils.bad_words import invitation_pattern

# from modules.management.verification.check_verification import CheckVerification

if TYPE_CHECKING:
    from core.navigator import Navigator
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from ui.yes_no_service.yes_no_factory import YesNoViewFactory
    from features.auto_moderation.verification.service import VerificationService


class Controller:
    def __init__(
            self,
            bot,
            settings: SettingsStorage,
            db_factory: DBFactory,
            navigator: Navigator,
            verification_service: VerificationService,
            yes_no_factory: YesNoViewFactory
    ):
        self.bot = bot
        self.settings = settings
        self.db_factory = db_factory
        self.yes_no_factory = yes_no_factory
        self.navigator = navigator
        self.verification_service = verification_service

        bot.add_listener(self.on_ready)
        bot.add_listener(self.on_message)
        bot.add_listener(self.on_member_join)
        bot.add_listener(self.on_member_remove)
        bot.add_listener(self.on_guild_remove)
        bot.add_listener(self.on_guild_join)

    # --------------------------- EVENTS --------------------------- #
    async def on_ready(self) -> None:
        print(f'Ми приєдналися як {self.bot.user.name}')
        # await CheckVerification(parent=self).prepare()

        # if not self.daily_birthday_check.is_running():
        #     self.daily_birthday_check.start()
        await self.settings.load_all_guilds_settings()

        flow = VerificationFlow(
            bot=self.bot,
            settings=self.settings,
            yes_no_factory=self.yes_no_factory,
            service=self.verification_service
        )
        await flow.prepare_verification_channel()

    async def on_message(self, message) -> None:
        # TODO: потрібно зробити перевірку суперюзерів з бд
        # TODO: потрібно переписати on_message, зробити більш простим та читабельним

        if message.author.bot:
            return

        # if message.guild:
        #     nick = message.author.nick if message.author.nick else message.author.name
        #
        #     if invitation_pattern.search(message.content):
        #         await invitation_check(nick, message)
        #
        #     cleaned_message = bad_words.remove_punctuation(message.content.lower())
        #     original_message = cleaned_message
        #     cleaned_message = bad_words.replace_similar_chars(cleaned_message)
        #
        #     if blacklist_word_pattern.search(cleaned_message):
        #         await bad_words.check_for_bad_words(message, nick)
        #     elif blacklist_word_pattern.search(original_message):
        #         await bad_words.check_for_bad_words(message, nick)
        #
        #     if blacklist_games_pattern.search(cleaned_message):
        #         await handle_bad_games(message, nick)
        #     elif blacklist_games_pattern.search(original_message):
        #         await handle_bad_games(message, nick)
        #
        #     if len(message.content) > 5 and is_caps(message.content):
        #         await message.delete()
        #         await message.channel.send(f"```{nick}, please stop using the caps.```")
        #         return
        #
        #     await handle_spam(message)
        #
        # await self.handle_message(message)

    async def on_member_join(self, member) -> None:
        await UserJoinBirthdayService(self).check_if_birthday(member=member)  # TODO: правильно назвати імя функції

    async def on_member_remove(self, member) -> None:
        await MemberLeftNotification(bot=self.bot, settings=self.settings).check_if_notification(member)

    async def on_guild_remove(self, guild: discord.Guild) -> None:
        print(f'Бот від\'єднався від {guild.name}')
        delete_guild_scenario = self.db_factory.for_cleanup_guild(guild.id)
        await delete_guild_scenario.db_proceed()

    async def on_guild_join(self, guild: discord.Guild) -> None:
        print(f'бот приєднався до {guild.name}')
        scenario = self.db_factory.for_init_guild(guild.id)
        await scenario.db_proceed()

    # --------------------------- LOOPS ---------------------------

    # @tasks.loop(hours=24)
    # async def daily_birthday_check(self) -> None:
    #     await self.birthday_manager.check_daily_birthday()
    #
    # # --------------------------- MESSAGE HANDLING ---------------------------
    #
    # async def handle_message(self, message):
    #     ...
