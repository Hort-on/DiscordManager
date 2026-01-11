import random

import discord


class RandomTeamManualService:
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

    async def random_team_proceed(
            self,
            interaction: discord.Interaction,
            users_list: str,
            teams_quantity: int
    ) -> None:
        members = [m.strip() for m in users_list.split(',')]

        if teams_quantity > len(members):
            await interaction.edit_original_response(
                content='```❌ Teams count cannot be greater than users count```',
            )
            return

        random.shuffle(members)

        teams = [[] for _ in range(teams_quantity)]

        for i, member in enumerate(members):
            teams[i % teams_quantity].append(member)

        embed = self._build_embed(teams)

        await interaction.followup.send(embed=embed, ephemeral=False)
