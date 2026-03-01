from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from ui.embed_constructor.embed_constructor import ErrorEmbed

if TYPE_CHECKING:
    from features.for_everyone.randomizer.flow import RandomizerFlow


class RandomNumModal(discord.ui.Modal, title='Random number'):
    def __init__(self, flow: RandomizerFlow):
        super().__init__()
        self.flow = flow

    first_num = discord.ui.TextInput(
        label='First number',
        placeholder='Please enter the first number min 0',
        required=True
    )

    second_num = discord.ui.TextInput(
        label='Second number',
        placeholder='Please enter a number min 1',
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        try:
            number_1 = int(self.first_num.value)
            number_2 = int(self.second_num.value)
        except ValueError:
            embed = ErrorEmbed(
                description='The numbers must be written in digits.'
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await self.flow.for_number_proceed(
            interaction=interaction,
            first_num=number_1,
            second_num=number_2
        )


class RandomWordModal(discord.ui.Modal, title='Random word'):
    def __init__(self, flow: RandomizerFlow):
        super().__init__()
        self.flow = flow

    words = discord.ui.TextInput(
        label='Words',
        placeholder='Please enter words separated by coma',
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.flow.for_word_proceed(
            interaction=interaction,
            words_list=self.words.value
        )


class RandomTeamByTextModal(discord.ui.Modal, title='Random teams manual'):
    def __init__(self, flow: RandomizerFlow):
        super().__init__()
        self.flow = flow

    users_list = discord.ui.TextInput(
        label='List of users',
        placeholder='Please enter user names separated by coma',
        required=True
    )

    teams_quantity = discord.ui.TextInput(
        label='Teams quantity',
        placeholder='Please enter a number of commands',
        required=True,
        max_length=2
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        try:
            quantity = int(self.teams_quantity.value)
        except ValueError:
            embed = ErrorEmbed(
                description='The number must be written in digits.'
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await self.flow.team_by_text_proceed(
            interaction=interaction,
            users_list=self.users_list.value,
            teams_quantity=quantity
        )


class RandomTeamByChannelModal(discord.ui.Modal, title='Random teams automatically'):
    def __init__(self, channel, flow: RandomizerFlow):
        super().__init__()
        self.channel = channel
        self.flow = flow

    teams_quantity = discord.ui.TextInput(
        label='Teams quantity',
        placeholder='Please enter a number of teams',
        required=True,
        max_length=2
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        try:
            quantity = int(self.teams_quantity.value)
        except ValueError:
            embed = ErrorEmbed(
                description='The number must be written in digits.'
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await self.flow.team_by_channel_proceed(
            interaction=interaction,
            channel=self.channel,
            teams_quantity=quantity
        )
