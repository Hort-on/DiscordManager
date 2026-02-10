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

from modules.buttons.for_admins.edit_settings_buttons.services.settings_formatter import SettingsFormatter

from services.drop_down_menu.drop_down_selector import DropMenuView
from services.embed_constructor.embed_constructor import SuccessEmbed, ErrorEmbed, InfoEmbed
from services.buttons.navigator_context import NavigationContext


def build_options(guild_id: int) -> list[discord.SelectOption]:
    container: BotContainer = AppContainer.get()

    sys_channels = container.settings.dict_storage.for_dict_get(
        target=StorageTarget.SYSTEM_CHANNELS,
        guild_id=guild_id
    )

    return [
        discord.SelectOption(
            label=key.removesuffix('_id').replace('_', ' '),
            value=key
        )
        for key in sorted(sys_channels.keys(), key=lambda item: item[0])
    ]


class AddSystemChannelsService:
    def __init__(self, navigator: Navigator):
        container: BotContainer = AppContainer.get()

        self.db_factory: DBFactory = container.db_factory
        self.settings: SettingsStorage = container.settings
        self.navigator = navigator

        self.ch_key = None

    async def choosing_the_channel(self, interaction: discord.Interaction, ch_key: str):
        self.ch_key = ch_key[0]

        options = [
            discord.SelectOption(
                label=ch.name,
                value=str(ch.id)
            )
            for ch in sorted(
                interaction.guild.text_channels,
                key=lambda ch: ch.name.lower()
            )
        ]

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the channel',
            callback=self._save_result
        )

        context = getattr(view, 'context', NavigationContext())

        context.push(target='settings_menu')

        view.context = context

        info_embed = InfoEmbed(
            description=f'Please select the channel you want to assign to'
                        f' {ch_key[0].removesuffix('_id').replace('_', ' ')}'
        )

        await interaction.response.edit_message(embed=info_embed, view=view)

    async def _save_result(self, interaction: discord.Interaction, config: str) -> None:
        ch_id = int(config[0])

        write = self.db_factory.for_write_data(
            guild_id=interaction.guild_id,
            table_name='sys_channels',
            data={self.ch_key: ch_id}
        )

        result = await write.db_proceed()

        if not result:
            error_embed = ErrorEmbed(
                description='Something went wrong, please try again later.'
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        self.settings.dict_storage.for_dict_update(
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=interaction.guild_id,
            data={self.ch_key: ch_id}
        )

        channel = interaction.guild.get_channel(ch_id)

        success_embed = SuccessEmbed(
            description=f'For {self.ch_key} successfully assigned the channel {channel.name}'
        )

        formatter = SettingsFormatter()
        current_channels = await formatter.format_current_system_channels(guild=interaction.guild)

        await interaction.response.edit_message(embeds=[success_embed, current_channels])


class DeleteSystemChannelsService:
    def __init__(self, navigator: Navigator):
        container: BotContainer = AppContainer.get()

        self.db_factory: DBFactory = container.db_factory
        self.settings: SettingsStorage = container.settings
        self.navigator = navigator

    async def delete_channel(self, interaction: discord.Interaction, values: list[str]) -> None:
        delete = self.db_factory.for_cleanup_system_channel(
            guild_id=interaction.guild_id,
            channels=values
        )

        result = await delete.db_proceed()
        if not result:
            error_embed = ErrorEmbed(
                description='Something went wrong, please try again later.'
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        channel_keys = [ch for ch in values]

        self.settings.dict_storage.for_dict_update(
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=interaction.guild_id,
            data={key: None for key in channel_keys}
        )

        is_plural = len(values) != 1

        word_1 = 'Channels' if is_plural else 'Channel'
        word_2 = 'have' if is_plural else 'has'

        msg = f'{word_1} {word_2} been successfully deleted.'

        success_embed = SuccessEmbed(
            description=msg
        )

        formatter = SettingsFormatter()
        current_channels = await formatter.format_current_system_channels(guild=interaction.guild)

        await interaction.response.edit_message(embeds=[success_embed, current_channels])
