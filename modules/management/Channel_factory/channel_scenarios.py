from database.db_factory.db_scenario_factory import DBScenarioFactory
from modules.buttons.buttons_for_admins.delete_message_button.delete_any_message.service.DeleteMessageModal import \
    DeleteMessagesModal


class ChannelScenario:
    async def channel_proceed(self, interaction, channel):
        raise NotImplementedError


class SaveChannelToDBForMessageScenario(ChannelScenario):
    def __init__(
            self,
            db: DBScenarioFactory
    ):

        self.db = db

    async def on_channel_selected(
            self,
            interaction,
            channel
    ) -> bool:

        return await self.db.write_data(
            interaction.guild.id,
            'channels',
            {
                'guild_id': interaction.guild.id,
                'user_id': interaction.user.id,
                'channel_id': channel.id
            }
        )


class SaveChannelToDBScenario(ChannelScenario):
    def __init__(
            self,
            db: DBScenarioFactory,
            config_key
    ):

        self.db = db
        self.config_key = config_key

    async def channel_proceed(
            self,
            interaction,
            channel
    ) -> bool:

        return await self.db.write_data(
            interaction.guild.id,
            'settings',
            {
                f'{self.config_key}_id': channel.id
            }
        )


class WizardScenario(ChannelScenario):
    def __init__(
            self,
            parent,
            db: DBScenarioFactory,
            config_key
    ):

        self.parent = parent
        self.db = db
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
