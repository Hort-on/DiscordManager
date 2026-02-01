from __future__ import annotations

from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from core.container import BotContainer
    from services.factories.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from services.buttons.navigator import Navigator

from core.container import AppContainer

from database.settings_storage.settings_manager import StorageTarget

from modules.buttons.for_admins.edit_settings_buttons.settings_formatter import SettingsFormatter

from services.embed_constructor.embed_constructor import SuccessEmbed, ErrorEmbed


class SystemChannelsService:
    def __init__(self, navigator: Navigator):
        container: BotContainer = AppContainer.get()

        self.db_factory: DBFactory = container.db_factory
        self.settings: SettingsStorage = container.settings
        self.navigator = navigator

    def build_options(self, guild_id: int):
        sys_channels = self.settings.dict_storage.for_dict_get_all(
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild_id
        )

        return [
            discord.SelectOption(
                label=k.replace('_', ' ').title(),
                value=k
            )
            for k, v in sorted(sys_channels.items(), key=lambda item: item[0])
        ]

    async def save_main_data(self, interaction: discord.Interaction, config_key: str):
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

        db_result = await write.db_proceed()

        self.settings.dict_storage.for_dict_set(
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id,
            key=config_key[0],
            value=new_value
        )

        success_embed = SuccessEmbed(
            description=f'{config_key[0]} is successfully {'enabled' if new_value else 'disabled'}'
        )

        error_embed = ErrorEmbed(
            description='Something went wrong, please try again later.'
        )

        formatter = SettingsFormatter()
        settings_embed = await formatter.format_current_main_settings(interaction)

        await interaction.response.edit_message(
            embeds=[settings_embed, success_embed if db_result else error_embed]
        )
