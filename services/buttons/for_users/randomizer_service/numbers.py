import random

import discord

from modules.buttons.for_users.randomizer.reshuffle import ReshuffleView


class RandomNumService:
    async def random_num_proceed(
            self,
            interaction: discord.Interaction,
            first_num: int,
            second_num: int
    ) -> None:
        result = random.randint(first_num, second_num)

        view = ReshuffleView(self.random_num_proceed, first_num, second_num)
        await interaction.edit_original_response(
            content=f'The number is: {result}',
            view=view
        )
