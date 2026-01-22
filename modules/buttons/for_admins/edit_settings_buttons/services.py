from __future__ import annotations

import discord

from modules.buttons.other_buttons.back import BackButton

from services.yes_no_view.view.yes_no import YesNoView
from services.factories.channel_factory.scenarios_factory import ChannelFactory
from services.other_services.get_channel import ChannelSelectorManager
from services.utils.format_result.scenarios_factory import ResultFactory
from services.utils.messages import EDIT_CONFIG_MSGS, SYSTEM_MSGS
from services.utils.option_list import SETTINGS_OPTIONS

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from services.yes_no_view.yes_no_view_factory.yes_no_factory import YesNoViewFactory
    from modules.buttons.navigator import Navigator


class ChoiceHandler:
    def __init__(self, yes_no_factory: 'YesNoViewFactory'):
        self.yes_no_factory = yes_no_factory

    async def choice_procedure(
            self,
            interaction: discord.Interaction,
            option_type: str,
            config_key: str
    ) -> None:

        match option_type:
            case 'boolean':
                scenario = self.yes_no_factory.for_confirmation(config_key=config_key)

                view = YesNoView(scenario=scenario)

                await interaction.edit_original_response(
                    content=EDIT_CONFIG_MSGS.get('editing_feature_msg').format(
                        feature={config_key.replace('_', ' ').title()}),
                    view=view
                )

            case 'channel':
                scenario = ChannelFactory.for_db_save(
                    config_key=config_key
                )

                manager = ChannelSelectorManager(
                    scenario=scenario,
                    text_only=True
                )

                await manager.select_channel_type(interaction=interaction)

            case _:
                await interaction.edit_original_response(
                    content=SYSTEM_MSGS.get('failure_msg')
                )
                return


class SettingSelector(discord.ui.Select):
    def __init__(self, yes_no_factory: 'YesNoViewFactory'):
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

        self.choice_handler = ChoiceHandler(yes_no_factory=yes_no_factory)

    async def callback(
            self,
            interaction: discord.Interaction
    ) -> None:

        config_key = self.values[0]
        option_type = SETTINGS_OPTIONS.get(config_key)

        if not option_type:
            await interaction.edit_original_response(
                content=''   # TODO: зробити embed
            )
            return

        await self.choice_handler.choice_procedure(
            interaction=interaction,
            option_type=option_type,
            config_key=config_key
        )


class SettingSelectorView(discord.ui.View):
    def __init__(self, navigator: Navigator, yes_no_factory: 'YesNoViewFactory'):
        super().__init__(timeout=None)

        self.add_item(SettingSelector())
        self.add_item(BackButton(target='admin_menu', navigator=navigator))


class SettingsFormatter:

    @staticmethod
    async def format_settings(interaction: discord.Interaction) -> None:
        scenario = ResultFactory.for_settings_edit()
        summary_result = scenario.build_result(interaction=interaction)

        await interaction.edit_original_response(
            content=f'\n\n{summary_result}\n\n'  # TODO: зробити embed
        )
