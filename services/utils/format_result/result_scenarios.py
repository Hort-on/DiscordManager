import discord

from database.settings_storage.settings_storage import SettingsStorage
from database.settings_storage.settings_storage_manager import StorageTarget

from services.utils.messages import CONFIG_MSGS as CM


class FormatResultBaseScenario:

    async def build_result(self, interaction: discord.Interaction):
        raise NotImplementedError


class EditSettingsResultScenario(FormatResultBaseScenario):
    def __init__(self, settings: SettingsStorage):
        self.settings = settings

    async def build_result(self, interaction: discord.Interaction) -> None:
        lines: list[str] = ['Your current settings:\n']

        settings = self.settings.dict_storage.get_for_dict_all(
            StorageTarget.SETTINGS,
            interaction.guild_id
        )

        if not settings:
            await interaction.edit_original_response(
                content=CM.get('no_configuration_msg')
            )
            return

        for key, value in settings.items():
            status = '✅ Enabled' if value else '❌ Disabled'
            lines.append(f'-> {key}: {status}')

        self._append_superusers(interaction, lines)
        await self._append_channels(interaction, lines)
        await self._send_result(interaction, lines)

    def _append_superusers(self, interaction, lines):
        users = self.settings.set_storage.get_for_set(
            StorageTarget.SUPERUSERS,
            interaction.guild_id
        )

        lines.append('\nSuperusers:')

        if not users:
            lines.append('-> not assigned')
            return

        for user_id in users:
            member = interaction.guild.get_member(user_id)
            name = member.display_name if member else f'Unknown ({user_id})'
            lines.append(f'-> {name}')

    async def _append_channels(self, interaction: discord.Interaction, lines) -> None:
        current_selected_channels = self.settings.dict_storage.get_for_dict_all(
            StorageTarget.SELECTED_CHANNELS,
            interaction.guild_id
        )

        lines.append('\n Channels:')

        for key, value in current_selected_channels.items():
            channel = interaction.client.get_channel(value)
            status = channel.name if channel is not None else '❌ Not assigned'
            ch_name = key.replace('_channel_id', ' channel')
            lines.append(f'-> {ch_name}: {status}')

    @staticmethod
    async def _send_result(interaction: discord.Interaction, lines) -> None:
        result_msg = '\n'.join(lines)
        await interaction.edit_original_response(
            content=result_msg
        )
