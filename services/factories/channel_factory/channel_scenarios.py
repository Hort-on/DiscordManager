import discord

from services.factories.db_factory.db_scenario_factory import DBScenarioFactory

from services.modals.random_modal.team_by_channel import RandomTeamByChannelModal
from services.utils.messages import DB_MSGS, SYSTEM_MSGS


class ChannelScenario:
    async def on_channel_selected(self, interaction: discord.Interaction, channel):
        raise NotImplementedError


class SaveChannelToDBForMessageScenario(ChannelScenario):
    def __init__(
            self,
            db_factory: DBScenarioFactory
    ):

        self.db_factory = db_factory

    async def on_channel_selected(
            self,
            interaction: discord.Interaction,
            channel
    ) -> None:

        write_data_scenario = self.db_factory.for_write_data(
            interaction.guild.id,
            'channels',
            {
                'guild_id': interaction.guild.id,
                'user_id': interaction.user.id,
                'channel_id': channel.id
            }
        )

        result = await write_data_scenario.db_proceed()
        if result:
            await interaction.edit_original_response(
                content=DB_MSGS.get('channel_successful_msg')
            )
            return

        await interaction.edit_original_response(
            content=SYSTEM_MSGS.get('failure_msg')
        )


class SaveChannelToDBScenario(ChannelScenario):
    def __init__(
            self,
            db_factory: DBScenarioFactory,
            config_key: str
    ):

        self.db_factory = db_factory
        self.config_key = config_key

    async def on_channel_selected(
            self,
            interaction: discord.Interaction,
            channel
    ) -> None:

        write_data_scenario = self.db_factory.for_write_data(
            interaction.guild.id,
            'settings',
            {
                f'{self.config_key}_id': channel.id
            }
        )

        result = await write_data_scenario.db_proceed()
        if result:
            await interaction.edit_original_response(
                content=DB_MSGS.get('channel_successful_msg')
            )
            return

        await interaction.edit_original_response(
            content=SYSTEM_MSGS.get('failure_msg')
        )


class DeleteMessagesScenario(ChannelScenario):
    def __init__(self, modal):
        self.modal = modal

    async def on_channel_selected(
            self,
            interaction: discord.Interaction,
            channel
    ) -> None:
        await interaction.response.send_modal(
            self.modal(channel)
        )


class RandomSelection(ChannelScenario):
    async def on_channel_selected(
            self,
            interaction: discord.Interaction,
            channel
    ) -> None:
        await interaction.response.send_modal(
            RandomTeamByChannelModal(channel)
        )
