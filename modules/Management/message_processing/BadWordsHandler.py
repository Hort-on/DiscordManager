import re
import time
import asyncio

from modules.logger.logger import Logger
from config import SUPERUSERS
from modules.administration.user_manager import UserManager

#TODO: треба оптимізувати роботу цього хендлера
class BadWordsHandler:
    def __init__(self):
        self.bad_word_warnings = {}
        self.warnings_lock = asyncio.Lock()

    @staticmethod
    def remove_punctuation(sentence: str) -> str:
        translation_table = str.maketrans("", "", "-_*`~'+=#%^&,.?()[]{}<>:;\\/")
        return sentence.translate(translation_table)

    @staticmethod
    def replace_similar_chars(sentence: str) -> str:
        simple_replacements_map = {
            # similar_chars_us:
            'a': 'а', 'c': 'с', 'e': 'е', 'i': 'і', 'o': 'о', 'p': 'р', 'x': 'х', 'y': 'у', 'k': 'к',
            # similar_chars_special:
            '1': 'і', '3': 'з', '9': 'я', '@': 'а', '4': 'а', '$': 'с', '|': 'і', '0': 'о', '!': 'і', 'X̌': 'х', 'х': 'х',
            'x̌': 'х', 'ý': 'у', 'ỳ': 'у', 'ŷ': 'у', 'ƴ': 'у', 'ÿ': 'у', 'Ū': 'u', 'ū': 'u', 'ŭ': 'u', 'ü': 'u', 'ú': 'u',
            'ù': 'u', 'ï': 'ї', 'ɛ': 'є',
        }

        similar_chars_ru = {
            'ы': 'и', 'и': 'і',
        }

        replacement_table = str.maketrans(simple_replacements_map)

        for spec_char, simple_char in replacement_table.items():
            if str(spec_char) in sentence:
                sentence = sentence.translate(replacement_table)

        for ru_char, ukr_char in similar_chars_ru.items():
            if ru_char in sentence:
                sentence = re.sub(fr'{ru_char}(?!\b)', ukr_char, sentence)

        return sentence

    @staticmethod
    def get_warning_message(nick: str, warning_level: int) -> str:
        messages = [
            f"```{nick}, please avoid using profanity, be polite!```",
            f"```{nick}, the use of profanity is prohibited on this server.```",
            f"```{nick}, for the next violation, you will be banned!```"
        ]

        return messages[min(warning_level - 1, 2)]


    async def check_for_bad_words(self, message, nick):
        guild_id = message.guild.id
        user_id = message.author.id

        state_key = (guild_id, user_id)

        await Logger.info(nick, message.content)
        await message.delete()

        if user_id in SUPERUSERS:
            return

        async with self.warnings_lock:
            current_time = time.time()
            warning_count, last_time = self.bad_word_warnings.get(state_key, (0, 0))

            if current_time - last_time > 600:
                warning_count = 0

            warning_count += 1

            if warning_count >= 3:
                await UserManager.block_user(message, 1, "usage of profanity")
                await message.channel.send(f"```The user: {nick}, has been banned for violation the rule: 1.1```")
                self.bad_word_warnings.pop(state_key, None)
            else:
                await message.channel.send(self.get_warning_message(nick, warning_count))
                self.bad_word_warnings[state_key] = (warning_count, current_time)
