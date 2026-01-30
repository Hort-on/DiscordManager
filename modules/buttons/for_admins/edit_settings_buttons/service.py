from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.container import BotContainer
    from services.factories.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from services.buttons.navigator import Navigator

import discord

from core.container import AppContainer

from database.settings_storage.settings_manager import StorageTarget

from modules.buttons.for_admins.edit_settings_buttons.settings_formatter import SettingsFormatter

from services.embed_constructor.embed_constructor import SuccessEmbed, ErrorEmbed
from services.factories.channel_factory.scenarios_factory import ChannelFactory
from services.other_services.get_channel import ChannelSelectorManager
from services.utils.option_list import SETTINGS_OPTIONS


class ToggleService:
    def __init__(self, navigator: Navigator):
        container: BotContainer = AppContainer.get()

        self.db_factory: DBFactory = container.db_factory
        self.settings: SettingsStorage = container.settings
        self.navigator = navigator

    @staticmethod
    def prepare_options():
        sorted_keys = sorted(
            SETTINGS_OPTIONS.keys(),
            key=lambda k: SETTINGS_OPTIONS[k] != 'boolean'
        )

        return [
            discord.SelectOption(
                label=k.replace('_', ' ').title(),
                value=k
            )
            for k in sorted_keys
        ]

    async def proceed(self, interaction: discord.Interaction, config_key: str):
        option_type = SETTINGS_OPTIONS.get(config_key[0])

        match option_type:
            case 'boolean':
                await self._save_data(
                    interaction=interaction,
                    config_key=config_key[0]
                )

            case 'channel':
                print('ми у кейсі channel')
                scenario = ChannelFactory.for_db_save(
                    config_key=config_key[0]
                )
                print('створили сценарій')

                manager = ChannelSelectorManager(
                    navigator=self.navigator,
                    scenario=scenario,
                    text_only=True
                )
                print('створили менеджер')
                await manager.select_channel_type(interaction=interaction)

            case _:
                raise ValueError('Unknown option_type')

    async def _save_data(self, interaction: discord.Interaction, config_key: str):
        current_value = self.settings.dict_storage.for_dict_get(
            config_key,
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id,
        )

        current = current_value.get(config_key, False)
        new_value = not current

        write = self.db_factory.for_write_data(
            guild_id=interaction.guild_id,
            table_name='settings',
            data={config_key: new_value}
        )

        db_result = await write.db_proceed()

        self.settings.dict_storage.for_dict_set(
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id,
            key=config_key,
            value=new_value
        )

        success_embed = SuccessEmbed(
            description=f'{config_key} is successfully {'enabled' if new_value else 'disabled'}'
        )

        error_embed = ErrorEmbed(
            description='Something went wrong, please try again later.'
        )

        formatter = SettingsFormatter()
        settings_embed = await formatter.format_settings(interaction)

        await interaction.response.edit_message(
            embeds=[settings_embed, success_embed if db_result else error_embed]
        )
