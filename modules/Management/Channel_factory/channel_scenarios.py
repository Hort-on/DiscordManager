from database.data_base_model import DB
from modules.Management.channels_processing.setting_permissions_for_the_channel import SetPermissions
from modules.buttons.buttons_for_admins.delete_message_button.delete_any_message.service.DeleteMessageModal import \
    DeleteMessagesModal


class ChannelScenario:
    async def on_channel_selected(self, interaction, channel):
        raise NotImplementedError


class SaveChannelToDBForMessageScenario(ChannelScenario):
    async def on_channel_selected(self, interaction, channel) -> bool:
        db = DB()
        return await db.write_data(
            interaction.guild.id,
            'channels',
            {
                'guild_id': interaction.guild.id,
                'user_id': interaction.user.id,
                'channel_id': channel.id
            }
        )


class SaveChannelToDBScenario(ChannelScenario):
    def __init__(self, config_key):
        self.config_key = config_key

    async def on_channel_selected(self, interaction, channel) -> bool:
        db = DB()
        return await db.write_data(
            interaction.guild.id,
            'settings',
            {
                f'{self.config_key}_id': channel.id
            }
        )


class PermissionsScenario(ChannelScenario):
    async def on_channel_selected(self, interaction, channel) -> None:
        handler = SetPermissions(channel)
        await handler.set_permissions_for_channel(interaction)


class WizardScenario(ChannelScenario):
    def __init__(self, parent, config_key):
        self.parent = parent
        self.config_key = config_key

    async def on_channel_selected(self, interaction, channel) -> None:
        self.parent.config[self.config_key] = channel.id
        await self.parent.next_step(interaction)


class CompositeScenario(ChannelScenario):
    def __init__(self, *scenarios):
        self.scenarios = scenarios

    async def on_channel_selected(self, interaction, channel) -> None:
        for scenario in self.scenarios:
            await scenario.on_channel_selected(interaction, channel)


class DeleteMessagesScenario(ChannelScenario):
    async def on_channel_selected(self, interaction, channel) -> None:
        await interaction.response.send_modal(
            DeleteMessagesModal(channel)
        )
