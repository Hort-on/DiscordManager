import discord

from modules.buttons.for_users.randomizer.services import (
    RandomNumService,
    RandomWordService,
    RandomTeamByChannelService,
    RandomTeamByMsgService
)


class RandomNumModal(discord.ui.Modal, title='Random number'):
    def __init__(self):
        super().__init__()
        self.random_proceed = RandomNumService()

    first_num = discord.ui.TextInput(
        label='First number',
        placeholder='Please enter the first number min 0',
        required=True,
        max_length=3
    )

    second_num = discord.ui.TextInput(
        label='Second number',
        placeholder='Please enter a number min 1',
        required=True,
        max_length=3
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.random_proceed.random_num_proceed(
            interaction,
            int(self.first_num.value),
            int(self.second_num.value)
        )


class RandomWordModal(discord.ui.Modal, title='Random word'):
    def __init__(self):
        super().__init__()
        self.random_proceed = RandomWordService()

    words = discord.ui.TextInput(
        label='Words',
        placeholder='Please enter words separated by coma',
        required=True,
        max_length=3
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.random_proceed.random_word_proceed(
            interaction,
            str(self.words.value)
        )


class RandomTeamByChannelModal(discord.ui.Modal, title='Random teams automatically'):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel
        self.random_proceed = RandomTeamByChannelService()

    teams_quantity = discord.ui.TextInput(
        label='Teams quantity',
        placeholder='Please enter a number of teams',
        required=True,
        max_length=2
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.random_proceed.team_by_channel_proceed(
            interaction,
            self.channel,
            int(self.teams_quantity.value)
        )


class RandomTeamByMsgModal(discord.ui.Modal, title='Random teams manual'):
    def __init__(self):
        super().__init__()
        self.random_proceed = RandomTeamByMsgService()

    users_list = discord.ui.TextInput(
        label='List of users',
        placeholder='Please enter user names separated by coma',
        required=True,
        max_length=3
    )

    teams_quantity = discord.ui.TextInput(
        label='Teams quantity',
        placeholder='Please enter a number of commands',
        required=True,
        max_length=3
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.random_proceed.team_by_text_proceed(
            interaction,
            str(self.users_list.value),
            int(self.teams_quantity.value)
        )
