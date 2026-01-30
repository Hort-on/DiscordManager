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

from services.embed_constructor.embed_constructor import SuccessEmbed
from services.factories.channel_factory.scenarios_factory import ChannelFactory
from services.other_services.get_channel import ChannelSelectorManager
from services.utils.messages import EDIT_CONFIG_MSGS
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
        option_type = SETTINGS_OPTIONS.get(config_key)

        match option_type:
            case 'boolean':
                await self._save_data(
                    interaction=interaction,
                    config_key=config_key
                )

            case 'channel':
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

    async def _save_data(self, interaction: discord.Interaction, config_key: str):
        current = self.settings.dict_storage.for_dict_get(
            config_key,
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id,
        )

        new_value = not bool(current)

        write = self.db_factory.for_write_data(
            guild_id=interaction.guild_id,
            table_name='settings',
            data={config_key: new_value}
        )

        await write.db_proceed()

        self.settings.dict_storage.for_dict_set(
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id,
            key=config_key,
            value=new_value
        )

        embed = SuccessEmbed(
            description=f'{config_key}` {'enabled' if new_value else 'disabled'}'
        )

        await interaction.response.edit_message(embed=embed)
