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
    from general_services.translator.translator import Translator


class RandomizerFlow:
    def __init__(self, navigator: Navigator, service: RandomizerService, translator: Translator):
        self.navigator = navigator
        self.service = service
        self.translator = translator

    async def for_number_start(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(
            RandomNumModal(
                flow=self,
                translator=self.translator,
                guild_id=interaction.guild_id
            )
        )

    async def for_number_proceed(
            self,
            interaction: discord.Interaction,
            first_num: int,
            second_num: int,
            edit_mode: bool = False
    ):
        await interaction.response.defer(ephemeral=True)

        if first_num == second_num:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=interaction.guild_id,
                    section='RANDOMIZER',
                    key='different_numbers'
                )
            )
            await interaction.followup.send(embed=error_embed, ephemeral=True)
            return

        result = random.randint(first_num, second_num)
        view = ReshuffleView(
            first_num,
            second_num,
            callback=self.for_number_proceed,
            translator=self.translator,
            guild_id=interaction.guild_id
        )

        result_msg = self.translator.t(
            guild_id=interaction.guild_id,
            section='RANDOMIZER',
            key='num_result_msg',
            result=result
        )

        if edit_mode:
            await interaction.edit_original_response(content=result_msg, view=view)
        else:
            await interaction.followup.send(content=result_msg, view=view, ephemeral=True)

    async def for_word_start(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(
            RandomWordModal(
                flow=self,
                translator=self.translator,
                guild_id=interaction.guild_id
            )
        )

    async def for_word_proceed(
            self,
            interaction: discord.Interaction,
            words_list: str,
            edit_mode: bool = False
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        words = [w for w in words_list.split(',')]
        random.shuffle(words)

        if len(words) < 2:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=interaction.guild_id,
                    section='RANDOMIZER',
                    key='two_words',
                )
            )
            await interaction.followup.send(embed=error_embed, ephemeral=True)
            return

        chosen_word = random.choice(words)
        view = ReshuffleView(
            words_list,
            callback=self.for_word_proceed,
            translator=self.translator,
            guild_id=interaction.guild_id
        )

        result_msg = self.translator.t(
            guild_id=interaction.guild_id,
            section='RANDOMIZER',
            key='word_result_msg',
            chosen_word=chosen_word
        )

        if edit_mode:
            await interaction.edit_original_response(content=result_msg, view=view)
        else:
            await interaction.followup.send(content=result_msg, view=view, ephemeral=True)

    async def for_teams_by_text_start(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(
            RandomTeamByTextModal(
                flow=self,
                translator=self.translator,
                guild_id=interaction.guild_id
            )
        )

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
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=interaction.guild_id,
                    section='RANDOMIZER',
                    key='wrong_team_count'
                )
            )
            await interaction.followup.send(embed=error_embed)
            return

        teams = self.service.build_teams_by_text(members=members, teams_quantity=teams_quantity)

        embed = self._build_embed(teams=teams, guild_id=interaction.guild_id)

        view = ReshuffleView(
            users_list,
            teams_quantity,
            callback=self.team_by_text_proceed,
            translator=self.translator,
            guild_id=interaction.guild_id
        )

        if edit_mode:
            await interaction.edit_original_response(embed=embed, view=view)
        else:
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)

    async def for_teams_by_channel_start(self, interaction: discord.Interaction) -> None:
        options = self._get_channels(guild=interaction.guild)

        if not options:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=interaction.guild_id,
                    section='RANDOMIZER',
                    key='no_v_channels_found'
                )
            )

            await interaction.response.edit_message(embed=error_embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            translator=self.translator,
            guild_id=interaction.guild_id,
            placeholder=self.translator.t(
                guild_id=interaction.guild_id,
                section='SYSTEM_GENERAL',
                key='ask_for_channel'
            ),
            callback=self._proceed_channel
        )

        await interaction.response.edit_message(view=view)

    async def _proceed_channel(self, interaction: discord.Interaction, value: list[str]) -> None:
        channel_id = int(value[0])
        channel = interaction.client.get_channel(channel_id)

        await interaction.response.send_modal(
            RandomTeamByChannelModal(
                channel=channel,
                flow=self,
                translator=self.translator,
                guild_id=interaction.guild_id
            )
        )

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
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=interaction.guild_id,
                    section='RANDOMIZER',
                    key='wrong_team_count_txt'
                )
            )
            await interaction.followup.send(embed=error_embed)
            return

        teams = self.service.team_by_channel_proceed(members=members, teams_quantity=teams_quantity)

        embed = self._build_embed(teams=teams, guild_id=interaction.guild_id)

        view = ReshuffleView(
            channel,
            teams_quantity,
            callback=self.team_by_channel_proceed,
            translator=self.translator,
            guild_id=interaction.guild_id
        )

        if edit_mode:
            await interaction.edit_original_response(embed=embed, view=view)
        else:
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)

    def _get_channels(self, guild: discord.Guild) -> list[discord.SelectOption]:
        hidden_channels = self.service.get_hidden_channels(guild_id=guild.id)
        available_channels = guild.voice_channels

        return [
            discord.SelectOption(
                label=ch.name,
                value=str(ch.id)
            )
            for ch in available_channels if ch not in hidden_channels and len(ch.members) >= 2
        ]

    def _build_embed(self, teams: list[list[str]], guild_id: int) -> discord.Embed:
        embed = discord.Embed(
            title=self.translator.t(
                guild_id=guild_id,
                section='RANDOMIZER',
                key='team_distribution'
            ),
            color=discord.Color.blurple()
        )

        for idx, team in enumerate(teams, start=1):
            members_text = '\n'.join(
                f'🔸 {member}'
                for member in team
            ) or '—'

            embed.add_field(
                name=self.translator.t(
                    guild_id=guild_id,
                    section='RANDOMIZER',
                    key='team',
                    idx=idx
                ),
                value=members_text,
                inline=False
            )

        return embed
