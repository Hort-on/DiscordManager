import discord

from modules.management.channels_processing.getting_channel import ChannelTypeView
from services.factories.channel_factory.channel_scenario_factory import ChannelScenarioFactory
from services.modals.random_modal.RandomTeamManualModal import RandomTeamManualModal
from services.modals.random_modal.RandomNumModal import RandomNumModal
from services.modals.random_modal.RandomWordModal import RandomWordModal


class RandomModeView(discord.ui.View):
    @discord.ui.button(
        label='Random number',
        style=discord.ButtonStyle.blurple
    )
    async def random_num(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button
    ) -> None:
        await interaction.send_modal(RandomNumModal())

    @discord.ui.button(
        label='Random word',
        style=discord.ButtonStyle.blurple
    )
    async def random_word(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button
    ) -> None:
        await interaction.send_modal(RandomWordModal())

    @discord.ui.button(
        label='Random team manually',
        style=discord.ButtonStyle.blurple
    )
    async def random_team_manual(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button
    ) -> None:
        await interaction.send_modal(RandomTeamManualModal())

    @discord.ui.button(
        label='Random team automatically',
        style=discord.ButtonStyle.blurple
    )
    async def random_teams_auto(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button
    ) -> None:
        scenario = ChannelScenarioFactory.for_random_selection()

        await interaction.edit_original_response(
            content='```Please select the channel.```',
            view=ChannelTypeView(scenario, channels_with_users_only=True)
        )
