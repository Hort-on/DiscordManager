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


class AddSystemChannelsService:
    def __init__(self, navigator: Navigator):
        container: BotContainer = AppContainer.get()

        self.db_factory: DBFactory = container.db_factory
        self.settings: SettingsStorage = container.settings
        self.navigator = navigator

        self.ch_key = None

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
            placeholder='Please choose the channel',
            callback=self._save_result
        )

        context = getattr(view, 'context', NavigationContext())

        context.push(target='settings_menu')

        view.context = context

        await interaction.response.edit_message(view=view)

    async def _save_result(self, interaction: discord.Interaction, config: str):
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

        self.settings.dict_storage.for_dict_set(
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=interaction.guild_id,
            key=self.ch_key,
            value=ch_id
        )

        channel = interaction.guild.get_channel(ch_id)

        success_embed = SuccessEmbed(
            description=f'For {self.ch_key} successfully assigned the channel {channel.name}'
        )
        formatter = SettingsFormatter()
        current_channels = formatter.format_current_system_channels(guild=interaction.guild)

        await interaction.response.edit_message(embeds=[success_embed, current_channels[0], current_channels[1]])


class DeleteSystemChannelsService:
    def __init__(self, navigator: Navigator):
        container: BotContainer = AppContainer.get()

        self.db_factory: DBFactory = container.db_factory
        self.settings: SettingsStorage = container.settings
        self.navigator = navigator

    def channel_list(self, guild_id: int) -> discord.Embed:
        channels = self.settings.dict_storage.for_dict_get_all(
            target=StorageTarget.SYSTEM_CHANNELS,
            guild_id=guild_id
        )

        lines: list[str] = ['Current system channels:', f'{'-' * 26}']

        for k, v in sorted(channels.items(), key=lambda item: item[0]):
            lines.append(f'{k}: {v if v else '❗ not assigned.'}')

        return InfoEmbed(
            description='\n'.join(lines)
        )
