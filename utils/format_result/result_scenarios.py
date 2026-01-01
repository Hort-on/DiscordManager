import discord

from database.db_factory.db_scenario_factory import DBScenarioFactory
from database.settings_storage.settings_storage import SettingsStorage

from modules.configuration.starting_configuration import ConfigurationView

from utils.get_channel_name import get_channel_name
from utils.summary_fields import SUMMARY_FIELDS, CHANNEL_FIELDS
from utils.messages import CONFIG_MSGS as CM


class FormatResultBaseScenario:

    def result_proceed(self, interaction: discord.Interaction):
        raise NotImplementedError


class FirstConfirmationScenario(FormatResultBaseScenario):
    def __init__(
            self,
            parent: ConfigurationView
    ):
        self.parent = parent

    async def result_proceed(self, interaction: discord.Interaction) -> str:
        summary = ['Configuration completed!\n']

        for key, label in SUMMARY_FIELDS.items():
            value = self.parent.config.get(key, False)
            status = '✅ Enabled' if value else '❌ Disabled'
            summary.append(f"-> {label}: {status}")

        for key, label in CHANNEL_FIELDS.items():
            name = get_channel_name(interaction, self.parent.config.get(key))
            summary.append(f"-> {label}: {name}")

        summary_result = "\n".join(summary)

        return summary_result


class EditSettingsResultScenario(FormatResultBaseScenario):
    def __init__(self, db_factory: DBScenarioFactory, settings: SettingsStorage):
        self.settings = settings
        self.db_factory = db_factory

    async def result_proceed(self, interaction: discord.Interaction) -> str | None:
        summary = ['Your current settings:\n']

        current_settings = self.settings.get_guild_settings(interaction.guild_id)
        if not current_settings:
            await interaction.edit_original_response(
                content=CM.get('no_configuration_msg')
            )
            return None

        current_superusers = self.settings.get_guild_superusers(interaction.guild_id)

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

        return '\n'.join(summary)
