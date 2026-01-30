from __future__ import annotations

from typing import TYPE_CHECKING

from modules.buttons.for_admins.edit_settings_buttons.settings_formatter import SettingsFormatter

if TYPE_CHECKING:
    from core.container import BotContainer
    from services.factories.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from services.buttons.navigator import Navigator

import discord

from core.container import AppContainer

from database.settings_storage.settings_manager import StorageTarget

from services.embed_constructor.embed_constructor import SuccessEmbed
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
        return [
            discord.SelectOption(
                label=key.replace('_', ' ').title(),
                value=key
            )
            for key in SETTINGS_OPTIONS.keys()
        ]

    async def proceed(
            self,
            interaction: discord.Interaction,
            config_key: str
    ):
        print('Ми у proceed')
        print(config_key)
        option_type = SETTINGS_OPTIONS.get(config_key[0])
        print('Отримали option_type')

        match option_type:
            case 'boolean':
                print('ми у кейсі boolean')
                await self._save_data(
                    interaction=interaction,
                    config_key=config_key
                )
                print('запустили _save_data')

            case 'channel':
                print('ми у кейсі channel')
                scenario = ChannelFactory.for_db_save(
                    config_key=config_key
                )

                manager = ChannelSelectorManager(
                    navigator=self.navigator,
                    scenario=scenario,
                    text_only=True
                )

                await manager.select_channel_type()

            case _:
                raise ValueError('Unknown option_type')

        print('Пройшли усі кейси')

    async def _save_data(self, interaction: discord.Interaction, config_key: str):
        print('ми у _save_data')
        current_value = self.settings.dict_storage.for_dict_get(
            config_key[0],
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id,
        )

        current = current_value.get(config_key[0], False)
        new_value = not current

        write = self.db_factory.for_write_data(
            guild_id=interaction.guild_id,
            table_name='settings',
            data={config_key[0]: new_value}
        )

        await write.db_proceed()

        self.settings.dict_storage.for_dict_set(
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id,
            key=config_key[0],
            value=new_value
        )
        print(self.settings._guild_settings)

        embed = SuccessEmbed(
            description=f'{config_key[0]} is successfully {'enabled' if new_value else 'disabled'}'
        )
        formatter = SettingsFormatter()
        settings_embed = await formatter.format_settings(interaction)

        await interaction.response.edit_message(embeds=[settings_embed, embed])
