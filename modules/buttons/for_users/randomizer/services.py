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
        await interaction.response.edit_message(
            content=f'The number is: {result}',
            view=view
        )


class RandomWordService:
    async def random_word_proceed(
            self,
            interaction: discord.Interaction,
            words_list: str
    ) -> None:
        words = [w.strip() for w in words_list.strip(',')]
        result = random.choice(words)

        view = ReshuffleView(self.random_word_proceed, words)

        await interaction.response.edit_message(
            content=f'The word is: {result}',
            view=view
        )


class RandomTeamByMsgService:
    @staticmethod
    def _build_embed(teams: list[list[str]]) -> discord.Embed:
        embed = discord.Embed(
            title='🎲 Random Team Distribution',
            color=discord.Color.blurple()
        )

        for idx, team in enumerate(teams, start=1):
            members_text = '\n'.join(
                f'-> {member}'
                for member in team
            ) or '—'

            embed.add_field(
                name=f'TEAM {idx}',
                value=members_text,
                inline=False
            )

        return embed

    async def team_by_text_proceed(
            self,
            interaction: discord.Interaction,
            users_list: str,
            teams_quantity: int
    ) -> None:
        members = [m.strip() for m in users_list.split(',')]

        if teams_quantity > len(members):
            await interaction.response.edit_message(
                content='```❌ Teams count cannot be greater than users count```',
            )
            return

        random.shuffle(members)

        teams = [[] for _ in range(teams_quantity)]

        for i, member in enumerate(members):
            teams[i % teams_quantity].append(member)

        embed = self._build_embed(teams)

        view = ReshuffleView(self.team_by_text_proceed, users_list, teams_quantity)

        if not interaction.response.is_done():
            await interaction.followup.send(embed=embed, view=view, ephemeral=False)
            return

        await interaction.response.edit_message(embed=embed, view=view)


class RandomTeamByChannelService:
    @staticmethod
    def _build_embed(teams: list[list[discord.Member]]) -> discord.Embed:
        embed = discord.Embed(
            title='🎲 Random Team Distribution',
            color=discord.Color.blurple()
        )

        for idx, team in enumerate(teams, start=1):
            members_text = '\n'.join(
                f'-> {member.display_name}'
                for member in team
            ) or '—'

            embed.add_field(
                name=f'TEAM {idx}',
                value=members_text,
                inline=False
            )

        return embed

    async def team_by_channel_proceed(
            self,
            interaction: discord.Interaction,
            channel,
            teams_quantity
    ) -> None:
        members = [m for m in channel.members if not m.bot]

        if teams_quantity > len(members):
            await interaction.response.edit_message(
                content='```❌ Teams count cannot be greater than users count```',
            )
            return

        random.shuffle(members)

        teams = [[] for _ in range(teams_quantity)]

        for i, member in enumerate(members):
            teams[i % teams_quantity].append(member)

        embed = self._build_embed(teams)

        view = ReshuffleView(self.team_by_channel_proceed, channel, teams_quantity)

        if not interaction.response.is_done():
            await interaction.followup.send(embed=embed, view=view, ephemeral=False)
            return

        await interaction.response.edit_message(embed=embed, view=view)
