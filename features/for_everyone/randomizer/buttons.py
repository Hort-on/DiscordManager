from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.params_containers import MainMenuParams
from core.navigator.routes import Route

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from features.for_everyone.randomizer.flow import RandomizerFlow


class RandomizerMenuButton(discord.ui.Button):
    def __init__(self, navigator: Navigator, context: NavigationContext):
        super().__init__(
            label='🎲 Randomizer',
            style=discord.ButtonStyle.blurple
        )

        self.navigator = navigator
        self.context = context

    async def callback(self, interaction: discord.Interaction) -> None:
        view = self.navigator.randomizer_menu()

        view.context = self.context

        self.context.push(
            target=Route.MAIN_MENU,
            params=MainMenuParams(
                guild_id=interaction.guild_id,
                user_id=interaction.user.id,
                owner_id=interaction.guild.owner_id
            )
        )

        await interaction.response.edit_message(view=view)


class RandomNumButton(discord.ui.Button):
    def __init__(self, flow: RandomizerFlow):
        super().__init__(
            label='Random number',
            style=discord.ButtonStyle.secondary
        )

        self.flow = flow

    async def callback(self, interaction: discord.Interaction) -> None:
        await self.flow.for_number_start(interaction=interaction)


class RandomWordButton(discord.ui.Button):
    def __init__(self, flow: RandomizerFlow):
        super().__init__(
            label='Random word',
            style=discord.ButtonStyle.secondary
        )

        self.flow = flow

    async def callback(self, interaction: discord.Interaction) -> None:
        await self.flow.for_word_start(interaction=interaction)


class RandomTeamByText(discord.ui.Button):
    def __init__(self, flow: RandomizerFlow):
        super().__init__(
            label='Random team by message',
            style=discord.ButtonStyle.secondary
        )

        self.flow = flow

    async def callback(self, interaction: discord.Interaction):
        await self.flow.for_teams_by_text_start(interaction=interaction)


class RandomTeamByChannel(discord.ui.Button):
    def __init__(self, navigator: Navigator, flow: RandomizerFlow):
        super().__init__(
            label='Random team by channel',
            style=discord.ButtonStyle.secondary
        )

        self.navigator = navigator
        self.flow = flow

    async def callback(self, interaction: discord.Interaction):
        await self.flow.for_teams_by_channel_start(interaction=interaction)
