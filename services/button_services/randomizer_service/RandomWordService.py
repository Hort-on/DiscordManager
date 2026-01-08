import random

import discord


class RandomWordService:

    @staticmethod
    async def random_word_proceed(
            interaction: discord.Interaction,
            words_list: str
    ) -> None:
        words = [w.strip() for w in words_list.strip(',')]
        result = random.choice(words)

        await interaction.edit_original_response(
            content=f'The word is: {result}'
        )
