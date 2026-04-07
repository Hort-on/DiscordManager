from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from ui.embed_constructor.embed_constructor import ErrorEmbed

if TYPE_CHECKING:
    from features.for_everyone.randomizer.flow import RandomizerFlow
    from general_services.translator.translator import Translator


class RandomNumModal(discord.ui.Modal):
    def __init__(self, flow: RandomizerFlow, translator: Translator, guild_id: int):
        super().__init__(
            title=translator.t(
                guild_id=guild_id, section="RANDOMIZER", key="random_number"
            )
        )
        self.flow = flow

        self.first_num = discord.ui.TextInput(
            label=translator.t(
                guild_id=guild_id, section="RANDOMIZER", key="first_num"
            ),
            placeholder=translator.t(
                guild_id=guild_id, section="RANDOMIZER", key="first_num_placeholder"
            ),
            required=True,
        )

        self.second_num = discord.ui.TextInput(
            label=translator.t(
                guild_id=guild_id, section="RANDOMIZER", key="second_num"
            ),
            placeholder=translator.t(
                guild_id=guild_id, section="RANDOMIZER", key="second_num_placeholder"
            ),
            required=True,
        )

        self.translator = translator
        self.add_item(self.first_num)
        self.add_item(self.second_num)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        assert guild is not None

        try:
            number_1 = int(self.first_num.value)
            number_2 = int(self.second_num.value)
        except ValueError:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=guild.id, section="RANDOMIZER", key="error_num"
                )
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return

        await self.flow.for_number_proceed(
            interaction=interaction, first_num=number_1, second_num=number_2
        )


class RandomWordModal(discord.ui.Modal):
    def __init__(self, flow: RandomizerFlow, translator: Translator, guild_id: int):
        super().__init__(
            title=translator.t(
                guild_id=guild_id, section="RANDOMIZER", key="random_word"
            )
        )
        self.flow = flow

        self.words = discord.ui.TextInput(
            label=translator.t(guild_id=guild_id, section="RANDOMIZER", key="words"),
            placeholder=translator.t(
                guild_id=guild_id, section="RANDOMIZER", key="words_placeholder"
            ),
            required=True,
        )

        self.add_item(self.words)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.flow.for_word_proceed(
            interaction=interaction, words_list=self.words.value
        )


class RandomTeamByTextModal(discord.ui.Modal):
    def __init__(self, flow: RandomizerFlow, translator: Translator, guild_id: int):
        super().__init__(
            title=translator.t(
                guild_id=guild_id, section="RANDOMIZER", key="random_team_msg"
            )
        )
        self.flow = flow

        self.users_list = discord.ui.TextInput(
            label=translator.t(
                guild_id=guild_id, section="RANDOMIZER", key="r_list_of_users"
            ),
            placeholder=translator.t(
                guild_id=guild_id, section="RANDOMIZER", key="r_ask_user_names"
            ),
            required=True,
        )

        self.teams_quantity = discord.ui.TextInput(
            label=translator.t(
                guild_id=guild_id, section="RANDOMIZER", key="r_team_quantity"
            ),
            placeholder=translator.t(
                guild_id=guild_id, section="RANDOMIZER", key="r_ask_number_of_teams"
            ),
            required=True,
            max_length=2,
        )

        self.translator = translator

        self.add_item(self.users_list)
        self.add_item(self.teams_quantity)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        assert guild is not None

        try:
            quantity = int(self.teams_quantity.value)
        except ValueError:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=guild.id, section="RANDOMIZER", key="error_num"
                )
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return

        await self.flow.team_by_text_proceed(
            interaction=interaction,
            users_list=self.users_list.value,
            teams_quantity=quantity,
        )


class RandomTeamByChannelModal(discord.ui.Modal):
    def __init__(
        self, channel, flow: RandomizerFlow, translator: Translator, guild_id: int
    ):
        super().__init__(
            title=translator.t(
                guild_id=guild_id, section="RANDOMIZER", key="random_team_сh"
            )
        )
        self.channel = channel
        self.flow = flow

        self.teams_quantity = discord.ui.TextInput(
            label=translator.t(
                guild_id=guild_id, section="RANDOMIZER", key="r_team_quantity"
            ),
            placeholder=translator.t(
                guild_id=guild_id, section="RANDOMIZER", key="r_ask_number_of_teams"
            ),
            required=True,
            max_length=2,
        )

        self.translator = translator

        self.add_item(self.teams_quantity)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        assert guild is not None

        try:
            quantity = int(self.teams_quantity.value)
        except ValueError:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=guild.id, section="RANDOMIZER", key="error_num"
                )
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return

        await self.flow.team_by_channel_proceed(
            interaction=interaction, channel=self.channel, teams_quantity=quantity
        )
