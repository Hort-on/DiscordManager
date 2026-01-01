import discord

from database.db_factory.db_scenario_factory import DBScenarioFactory
from modules.buttons.buttons_for_admins.delete_message_button.delete_any_message.service.DeleteMessageModal import \
    DeleteMessagesModal

from utils.messages import DB_MSGS, SYSTEM_MSGS


class ChannelScenario:
    async def channel_proceed(self, interaction: discord.Interaction, channel):
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

    async def channel_proceed(
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


class WizardScenario(ChannelScenario):
    def __init__(
            self,
            parent,
            db_factory: DBScenarioFactory,
            config_key
    ):

        self.parent = parent
        self.db_factory = db_factory
        self.config_key = config_key

    async def channel_proceed(
            self,
            interaction,
            channel
    ) -> None:

        self.parent.config[self.config_key] = channel.id
        await self.parent.next_step(interaction)


class CompositeScenario(ChannelScenario):
    def __init__(
            self,
            *scenarios
    ):

        self.scenarios = scenarios

    async def channel_proceed(
            self,
            interaction,
            channel
    ) -> None:

        for scenario in self.scenarios:
            await scenario.on_channel_selected(interaction, channel)


class DeleteMessagesScenario(ChannelScenario):
    async def channel_proceed(self, interaction, channel) -> None:
        await interaction.response.send_modal(
            DeleteMessagesModal(channel)
        )
