import discord

from database.settings_storage.settings_storage_manager import StorageTarget
from database.settings_storage.settings_storage import SettingsStorage

from services.factories.db_factory.db_scenario_factory import DBScenarioFactory

from services.utils.messages import CONFIG_MSGS as CM


class FormatResultBaseScenario:

    async def get_result_data(self, interaction: discord.Interaction):
        raise NotImplementedError


class EditSettingsResultScenario(FormatResultBaseScenario):
    def __init__(self, db_factory: DBScenarioFactory, settings: SettingsStorage):
        self.settings = settings
        self.db_factory = db_factory

    async def get_result_data(self, interaction: discord.Interaction) -> None:
        summary = ['Your current settings:\n']

        current_settings = self.settings.dict_storage.get_dict_all(
            StorageTarget.SETTINGS,
            interaction.guild_id
        )

        if not current_settings:
            await interaction.edit_original_response(
                content=CM.get('no_configuration_msg')
            )
            return None

        current_superusers = self.settings.set_storage.get_set(
            StorageTarget.SUPERUSERS,
            interaction.guild_id
        )

        for key, value in current_settings.items():
            status = '✅ Enabled' if value else '❌ Disabled'
            summary.append(f"-> {key}: {status}")

        if current_superusers:
            summary.append("\nSuperusers:")
            for user_id in current_superusers:
                member = interaction.guild.get_member(user_id)
                name = member.display_name
                summary.append(f"-> {name}")
        else:
            summary.append("\nSuperusers: not assigned!")

        await self._get_channels(interaction, summary)

    async def _get_channels(self, interaction: discord.Interaction, summary) -> None:
        current_selected_channels = self.settings.dict_storage.get_dict_all(
            StorageTarget.SELECTED_CHANNELS,
            interaction.guild_id
        )

        summary.append('\n Channels:')

        for key, value in current_selected_channels.items():
            channel = interaction.client.get_channel(value)
            status = channel.name if channel is not None else '❌ Not assigned'
            ch_name = key.replace('_channel_id', ' channel')
            summary.append(f'-> {ch_name}: {status}')

        await self._send_result(interaction, summary)

    @staticmethod
    async def _send_result(interaction: discord.Interaction, summary) -> None:
        await interaction.edit_original_response(
            content=summary
        )
