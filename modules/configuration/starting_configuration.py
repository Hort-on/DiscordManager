from typing import Any

import discord

from modules.Management.Channel_factory.channel_scenario_factory import ChannelScenarioFactory
from modules.Management.YesNoView.YesNoViewFactory.yes_no_scenario_factory import YesNoViewFactory
from modules.Management.YesNoView.view.YesNoView import YesNoView
from modules.Management.channels_processing.getting_channel import ChannelTypeView
from modules.configuration.superuser_procedure import SuperUserProcedure
from modules.configuration.finishing_configuration import FinishingConfiguration

from utils.start_config_steps import STEPS, STEP_DEPENDENCIES
from utils.messages import CONFIG_MESSAGES as CM

class ConfigurationView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.config = {}
        self.found_users = []
        self.not_found_users = []
        self.step_index = 0

    @discord.ui.button(label='Lets start', style=discord.ButtonStyle.green)
    async def start_configuration(self, interaction: discord.Interaction) -> None:
        scenario = YesNoViewFactory.for_start_config(self, on_decline_callback=self.cancel_configuration)
        view = YesNoView(scenario)

        await interaction.response.send_message(
            CM.get('initial_msg'),
            view=view,
            ephemeral=True
        )

    async def next_step(self, interaction: discord.Interaction) -> None:
        while self.step_index < len(STEPS):
            msg, config_key, view_type = STEPS[self.step_index]

            if not self.check_step(config_key):
                self.step_index += 1
                continue

            match view_type:
                case 'YesNoView':
                    scenario = YesNoViewFactory.for_start_config(parent=self, config_key=config_key)
                    view = YesNoView(scenario)

                    await interaction.edit_original_response(
                        content=CM.get(msg),
                        view=view,
                    )

                case 'ChannelTypeView':
                    scenario = ChannelScenarioFactory.for_wizard(parent=self, config_key=config_key)
                    view = ChannelTypeView(scenario)

                    await interaction.edit_original_response(
                        content=CM.get(msg),
                        view=view,
                    )

                case 'SuperUsers':
                    super_user_handler = SuperUserProcedure(self)
                    await super_user_handler.super_user_procedure(interaction)

            self.step_index += 1

        finishing_handler = FinishingConfiguration(self)
        await finishing_handler.finishing_configuration(interaction)
        return

    @staticmethod
    async def cancel_configuration(interaction: discord.Interaction):
        await interaction.edit_original_response(
            content=CM.get('canceled_msg'),
            view=None
        )

    def check_step(self, config_key):
        if not config_key:
            return True

        dependency = STEP_DEPENDENCIES.get(config_key)
        return self.config.get(dependency, True) if dependency else True
