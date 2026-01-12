import random

import discord

from modules.buttons.for_users.randomizer.reshuffle import ReshuffleView


class RandomWordService:
    async def random_word_proceed(
            self,
            interaction: discord.Interaction,
            words_list: str
    ) -> None:
        words = [w.strip() for w in words_list.strip(',')]
        result = random.choice(words)

        view = ReshuffleView(self.random_word_proceed, words)

        await interaction.edit_original_response(
            content=f'The word is: {result}',
            view=view
        )
