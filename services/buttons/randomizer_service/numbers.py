import random

import discord


class RandomNumService:

    @staticmethod
    async def random_num_proceed(
            interaction: discord.Interaction,
            first_num: int,
            second_num: int
    ) -> None:
        result = random.randint(first_num, second_num)

        await interaction.edit_original_response(
            content=f'The number is: {result}'
        )
