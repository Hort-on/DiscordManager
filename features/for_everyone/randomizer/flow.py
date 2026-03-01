from __future__ import annotations

import random

from typing import TYPE_CHECKING

import discord

from features.for_everyone.randomizer.modals import (
    RandomNumModal,
    RandomWordModal,
    RandomTeamByTextModal,
    RandomTeamByChannelModal
)
from features.for_everyone.randomizer.reshuffle_button import ReshuffleView

from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.embed_constructor.embed_constructor import ErrorEmbed

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_everyone.randomizer.services import RandomizerService


class RandomizerFlow:
    def __init__(self, navigator: Navigator, service: RandomizerService):

        self.navigator = navigator
        self.service = service

    async def for_number_start(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(RandomNumModal(flow=self))

    async def for_number_proceed(
            self,
            interaction: discord.Interaction,
            first_num: int,
            second_num: int,
            edit_mode: bool = False
    ):
        await interaction.response.defer(ephemeral=True)

        if first_num == second_num:
            embed = ErrorEmbed(
                description='The numbers must be different.'
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        result = random.randint(first_num, second_num)
        view = ReshuffleView(first_num, second_num, callback=self.for_number_proceed)

        if edit_mode:
            await interaction.edit_original_response(
                content=f'The number is: {result}',
                view=view
            )
        else:
            await interaction.followup.send(
                content=f'The number is: {result}',
                view=view,
                ephemeral=True
            )

    async def for_word_start(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(RandomWordModal(flow=self))

    async def for_word_proceed(
            self,
            interaction: discord.Interaction,
            words_list: str,
            edit_mode: bool = False
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        words = [w.strip() for w in words_list.split(',')]
        result = random.choice(words)

        if len(words) < 2:
            embed = ErrorEmbed(
                description='There must be at least 2 words'
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        chosen_word = random.choice(result)
        view = ReshuffleView(words_list, callback=self.for_word_proceed)

        if edit_mode:
            await interaction.edit_original_response(
                content=f'The word is: {chosen_word}',
                view=view
            )
        else:
            await interaction.followup.send(
                content=f'The word is: {chosen_word}',
                view=view,
                ephemeral=True
            )

    async def for_teams_by_text_start(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(RandomTeamByTextModal(flow=self))

    async def team_by_text_proceed(
            self,
            interaction: discord.Interaction,
            users_list: str,
            teams_quantity: int,
            edit_mode: bool = False
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        members = [m.strip() for m in users_list.split(',')]

        if teams_quantity > len(members):
            embed = ErrorEmbed(
                description='Teams count cannot be greater than users count.'
            )
            await interaction.followup.send(embed=embed)
            return

        teams = self.service.build_teams_by_text(
            members=members,
            teams_quantity=teams_quantity
        )

        embed = self._build_embed(
            teams=teams
        )

        view = ReshuffleView(users_list, teams_quantity, callback=self.team_by_text_proceed)

        if edit_mode:
            await interaction.edit_original_response(embed=embed, view=view)
        else:
            await interaction.followup.send(embed=embed, view=view)

    async def for_teams_by_channel_start(self, interaction: discord.Interaction) -> None:
        options = self._get_channels(guild=interaction.guild)

        if not options:
            error_embed = ErrorEmbed(
                description='No available voice channels found,'
                            ' most likely because no voice channels were found with more than 2 participants,'
                            ' or the server has no voice channels.'
            )

            await interaction.response.edit_message(embed=error_embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the channel:',
            callback=self._proceed_channel
        )

        await interaction.response.edit_message(view=view)

    async def _proceed_channel(self, interaction: discord.Interaction, value: list[str]) -> None:
        channel_id = int(value[0])
        channel = interaction.client.get_channel(channel_id)

        await interaction.response.send_modal(RandomTeamByChannelModal(
            channel=channel,
            flow=self
        ))

    async def team_by_channel_proceed(
            self,
            interaction: discord.Interaction,
            channel,
            teams_quantity: int,
            edit_mode: bool = False
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        members = [m for m in channel.members if not m.bot]

        if teams_quantity > len(members):
            embed = ErrorEmbed(
                description='Teams count cannot be greater than users count.'
            )
            await interaction.followup.send(embed=embed)
            return

        teams = self.service.team_by_channel_proceed(
            members=members,
            teams_quantity=teams_quantity
        )

        embed = self._build_embed(teams)

        view = ReshuffleView(channel, teams_quantity, callback=self.team_by_channel_proceed)

        if edit_mode:
            await interaction.edit_original_response(embed=embed, view=view)
        else:
            await interaction.followup.send(embed=embed, view=view)

    def _get_channels(self, guild: discord.Guild) -> list:
        hidden_channels = self.service.get_hidden_channels(guild_id=guild.id)
        available_channels = guild.voice_channels

        channels = [
            vc for vc in available_channels
            if len(vc.members) > 2
        ]

        return [channel for channel in channels if channel.id not in hidden_channels]

    @staticmethod
    def _build_embed(teams: list[list[str]]) -> discord.Embed:
        embed = discord.Embed(
            title='🎲 Random Team Distribution',
            color=discord.Color.blurple()
        )

        for idx, team in enumerate(teams, start=1):
            members_text = '\n'.join(
                f'🔸 {member}'
                for member in team
            ) or '—'

            embed.add_field(
                name=f'TEAM {idx}',
                value=members_text,
                inline=False
            )

        return embed
