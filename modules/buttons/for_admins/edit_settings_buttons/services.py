from __future__ import annotations

import discord

from core.container import AppContainer

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

from modules.buttons.other_buttons.back import BackButton

from services.yes_no_service.yes_no_view import YesNoView
from services.embed_constructor.embed_constructor import InfoEmbed, WarningEmbed
from services.factories.db_factory.db_scenario_factory import DBFactory
from services.factories.channel_factory.scenarios_factory import ChannelFactory
from services.other_services.get_channel import ChannelSelectorManager
from services.utils.messages import EDIT_CONFIG_MSGS, SYSTEM_MSGS
from services.utils.option_list import SETTINGS_OPTIONS

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.yes_no_service.yes_no_factory import YesNoViewFactory
    from services.buttons.navigator import Navigator
    from core.container import BotContainer


class ChoiceHandler:
    def __init__(
            self,
            db_factory: DBFactory,
            navigator: Navigator,
            yes_no_factory: YesNoViewFactory
    ):
        self.db_factory = db_factory
        self.navigator = navigator
        self.yes_no_factory = yes_no_factory

    async def choice_procedure(
            self,
            interaction: discord.Interaction,
            option_type: str,
            config_key: str
    ):
        print('Ми у ChoiceHandler перед матч кейсами')
        match option_type:
            case 'boolean':
                print('Кейс boolean')
                scenario = self.yes_no_factory.for_confirmation(
                    db_factory=self.db_factory,
                    navigator=self.navigator,
                    config_key=config_key
                )

                message = (EDIT_CONFIG_MSGS.get('editing_feature_msg')
                           .format(feature={config_key.replace('_', ' ').title()}))

                view = YesNoView(scenario=scenario)

                await interaction.response.edit_message(
                    content=message,
                    view=view
                )
                print('Кінець кейсу boolean')

            case 'channel':
                print('Кейс channel')
                scenario = ChannelFactory.for_db_save(
                    config_key=config_key
                )

                manager = ChannelSelectorManager(
                    scenario=scenario,
                    text_only=True
                )

                await manager.select_channel_type()
                return ''

            case _:
                print('Інший кейс')
                await interaction.response.edit_message(
                    content=SYSTEM_MSGS.get('failure_msg')
                )
                return


class SettingSelector(discord.ui.Select):
    def __init__(
            self,
            db_factory: DBFactory,
            navigator: Navigator,
            yes_no_factory: YesNoViewFactory
    ):
        super().__init__(
            placeholder='Please select a setting to edit...',
            options=[
                discord.SelectOption(
                    label=key.replace('_', ' ').title(),
                    value=key
                )
                for key in SETTINGS_OPTIONS.keys()
            ],
            min_values=1,
            max_values=1
        )

        self.choice_handler = ChoiceHandler(
            db_factory=db_factory,
            navigator=navigator,
            yes_no_factory=yes_no_factory
        )

    async def callback(
            self,
            interaction: discord.Interaction
    ) -> None:
        config_key = self.values[0]
        option_type = SETTINGS_OPTIONS.get(config_key)

        if not option_type:
            await interaction.response.edit_message(
                content=''  # TODO: зробити embed
            )
            return

        await self.choice_handler.choice_procedure(
            interaction=interaction,
            option_type=option_type,
            config_key=config_key
        )


class SettingSelectorView(discord.ui.View):
    def __init__(
            self,
            navigator: Navigator,
            db_factory: DBFactory,
            yes_no_factory: YesNoViewFactory
    ):
        super().__init__(timeout=None)

        self.add_item(SettingSelector(
            db_factory=db_factory,
            navigator=navigator,
            yes_no_factory=yes_no_factory
        ))
        self.add_item(BackButton(navigator=navigator))


class EditSettingsResultScenario:
    def __init__(self):
        container: BotContainer = AppContainer.get()
        self.settings: SettingsStorage = container.settings

    async def build_result(self, interaction: discord.Interaction) -> discord.Embed:
        settings = self.settings.dict_storage.for_dict_get_all(
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id
        )

        if not settings:
            return WarningEmbed(description='No settings found.')
        lines: list[str] = ['Setting                  Status', '-----------------------  ----------']
        # ---- SETTINGS TABLE ----

        for key, value in settings.items():
            if key == 'guild_id':
                continue
            status = '✅ Enabled' if value else '❌ Disabled'
            lines.append(f'🔸{key:<23}:  {status}')

        # ---- SUPERUSERS ----
        lines.append('')
        lines.append('Superusers:')
        users = self.settings.set_storage.for_set_get(
            StorageTarget.SUPERUSERS,
            interaction.guild_id
        )

        if not users:
            lines.append('❌ not assigned')
        else:
            for user_id in users:
                member = interaction.guild.get_member(user_id)
                name = member.display_name if member else f'Unknown ({user_id})'
                lines.append(f'🔸 {name}')

        # ---- CHANNELS ----
        lines.append('')
        lines.append('Channels:')

        current_selected_channels = self.settings.dict_storage.for_dict_get_all(
            StorageTarget.SELECTED_CHANNELS,
            interaction.guild_id
        )

        if not current_selected_channels:
            lines.append('❌ NOT ASSIGNED')
        else:
            for key, value in current_selected_channels.items():
                channel = interaction.client.get_channel(value)
                channel_name = channel.name if channel else '❌ Not assigned'
                ch_label = key.replace('_channel_id', '')
                lines.append(f'🔸 {ch_label}: {channel_name}')

        description = '```text\n' + '\n'.join(lines) + '\n```'

        return InfoEmbed(description=description)


class SettingsFormatter:
    @staticmethod
    async def format_settings(interaction: discord.Interaction) -> discord.Embed:
        embed = await EditSettingsResultScenario().build_result(interaction=interaction)
        return embed
