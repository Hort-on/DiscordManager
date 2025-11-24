import discord

from Modules.Management.getting_channel import ChannelTypeView
from Modules.Configuration.YesNoView import YesNoView
from Modules.Configuration.superuser_procedure import SuperUserProcedure
from Modules.Configuration.finishing_configuration import FinishingConfiguration

from db.steps import STEPS
from db.messages import CONFIG_MESSAGES as CM

class ConfigurationView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.config = {}
        self.found_users = []
        self.not_found_users = []
        self.step_index = 0

    @discord.ui.button(label='Lets start', style=discord.ButtonStyle.green)
    async def start_configuration(self, interaction: discord.Interaction):
        view = YesNoView(
            self,
            on_decline_callback=self.cancel_configuration
        )

        await interaction.response.send_message(
            CM.get('initial_msg'),
            view=view,
            ephemeral=True
        )

    async def next_step(self, interaction: discord.Interaction) -> None:
        """Обробляє поточний крок конфігурації"""
        if self.step_index >= len(STEPS):
            finishing_handler = FinishingConfiguration(self)
            await finishing_handler.finishing_configuration(interaction)
            return

        msg, config_key, view_type = STEPS[self.step_index]

        match view_type:
            case 'YesNoView':
                view = YesNoView(
                    parent=self,
                    config_key=config_key,
                )

                await interaction.response.send_message(
                    CM.get(msg),
                    view=view,
                    ephemeral=True,
                    delete_after=600
                )

            case 'ChannelTypeView':
                view = ChannelTypeView(
                    text_only=True,
                    parent=self,
                    config_key=config_key
                )

                await interaction.response.send_message(
                    CM.get(msg),
                    view=view,
                    ephemeral=True,
                    delete_after=600
                )

            case 'SuperUsers':
                super_user_handler = SuperUserProcedure(self)
                await super_user_handler.super_user_procedure(interaction)

        self.step_index += 1

    @staticmethod
    async def cancel_configuration(interaction: discord.Interaction):
        await interaction.response.send_message(
            CM.get('canceled_msg', 'no msg found for "cancel_configuration"'),
            ephemeral=True
        )
