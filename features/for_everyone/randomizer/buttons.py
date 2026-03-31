from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.params_containers import MainMenuParams
from core.navigator.routes import Route

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from features.for_everyone.randomizer.flow import RandomizerFlow
    from general_services.translator.translator import Translator


class RandomizerMenuButton(discord.ui.Button):
    def __init__(self, navigator: Navigator, context: NavigationContext, translator: Translator, guild_id: int):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='RANDOMIZER',
                key='randomizer_menu'
            ),
            style=discord.ButtonStyle.blurple
        )

        self.navigator = navigator
        self.context = context

    async def callback(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        assert guild is not None

        view = self.navigator.randomizer_menu(
            context=self.context,
            guild_id=guild.id
        )

        view.context = self.context

        self.context.push(
            target=Route.MAIN_MENU,
            params=MainMenuParams(
                guild_id=guild.id,
                user_id=interaction.user.id,
                owner_id=guild.owner_id
            )
        )

        await interaction.response.edit_message(view=view)


class RandomNumButton(discord.ui.Button):
    def __init__(self, flow: RandomizerFlow, translator: Translator, guild_id: int):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='RANDOMIZER',
                key='random_number'
            ),
            style=discord.ButtonStyle.secondary
        )

        self.flow = flow

    async def callback(self, interaction: discord.Interaction) -> None:
        await self.flow.for_number_start(interaction=interaction)


class RandomWordButton(discord.ui.Button):
    def __init__(self, flow: RandomizerFlow, translator: Translator, guild_id: int):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='RANDOMIZER',
                key='random_word'
            ),
            style=discord.ButtonStyle.secondary
        )

        self.flow = flow

    async def callback(self, interaction: discord.Interaction) -> None:
        await self.flow.for_word_start(interaction=interaction)


class RandomTeamByText(discord.ui.Button):
    def __init__(self, flow: RandomizerFlow, translator: Translator, guild_id: int):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='RANDOMIZER',
                key='random_team_msg'
            ),
            style=discord.ButtonStyle.secondary
        )

        self.flow = flow

    async def callback(self, interaction: discord.Interaction):
        await self.flow.for_teams_by_text_start(interaction=interaction)


class RandomTeamByChannel(discord.ui.Button):
    def __init__(self, navigator: Navigator, flow: RandomizerFlow, translator: Translator, guild_id: int):
        super().__init__(
            label=translator.t(
                guild_id=guild_id,
                section='RANDOMIZER',
                key='random_team_сh'
            ),
            style=discord.ButtonStyle.secondary
        )

        self.navigator = navigator
        self.flow = flow

    async def callback(self, interaction: discord.Interaction):
        await self.flow.for_teams_by_channel_start(interaction=interaction)
