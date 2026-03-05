from __future__ import annotations

from typing import TYPE_CHECKING

from collections import defaultdict, deque
import time

import discord

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage


class ContentModerationService:
    def __init__(self, db_factory: DBFactory, settings: SettingsStorage):

        self.db_factory = db_factory
        self.settings = settings

        self.violators_list = []

        self.user_spam = defaultdict(lambda: deque(maxlen=5))
        self.user_caps = defaultdict(lambda: deque(maxlen=5))

    def is_spam(self, message: discord.Message) -> bool:
        now = time.monotonic()

        key = (message.author.id, message.channel.id)

        timestamps = self.user_spam[key]
        timestamps.append(now)

        return len(timestamps) == 5 and (timestamps[-1] - timestamps[0] <= 5)

    def is_caps(self, message: discord.Message) -> bool:
        text = message.content
        total_chars = len(text)
        if total_chars == 0:
            return False

        uppercase_chars = sum(1 for char in text if char.isupper())
        uppercase_ratio = uppercase_chars / total_chars

        return uppercase_ratio >= 0.8

    def is_invitation(self, message: discord.Message) -> bool:
        ...

    def is_bad_word(self, message: discord.Message) -> bool:
        ...

    async def handle_spam(self, message):
        user_id = message.author.id
        current_time = time.timedelta()

        if user_id not in user_spam_data:
            user_spam_data[user_id] = {'messages': [], 'warnings': 0}

        user_data = user_spam_data[user_id]

        user_data['messages'].append(current_time)
        user_data['messages'] = [t for t in user_data['messages'] if current_time - t <= 3]

        msg_count = len(user_data['messages'])

        if msg_count == 3:
            user_data['warnings'] += 1
            await warn_spam(self, message)
        elif msg_count >= 5 and user_data['warnings'] >= 1:
            await UserManager.block_user(message, 5, 'Spam')
            user_data['warnings'] = 0
        elif msg_count >= 5:
            user_data['warnings'] += 1

    async def warn_spam(self, message):
        await message.delete()
        await message.channel.send(f'```{message.author.nick}, Please stop spamming otherwise you will be banned!```',
                                   delete_after=1200)

    async def invitation_check(self, nick, message):
        if message.author.id not in SUPERUSERS:
            await message.delete()
            await message.channel.send(
                f'```{nick}, advertising other servers without the administration\'s permission is prohibited on this server.```',
                delete_after=60)
            await logger("BOT", f'The user: {nick}, sent an invitation: {message.content}',
                         'logs/invitations.log')
        else:
            return

    def is_caps(self, text):


    async def handle_bad_games(self, message, nick):
        if message.channel.id == EXCLUDED_CHANNEL:  # TODO: добавити список каналів котрі будуть ігноруватись в бд
            return

        user_id = message.author.id
        is_repeat_offense = user_id in bad_games_warnings

        await message.delete()

        if is_repeat_offense:
            bad_games_warnings.discard(user_id)
            await UserManager.block_user(message, 60, "Violation of the rules", True)
        else:
            bad_games_warnings.add(user_id)
            # TODO: зробити окремий функціонал для заборонених ігор
            warning = f"```{nick}, discussion, mention, or advertisement of russian games is prohibited!```"
            await message.channel.send(warning)

