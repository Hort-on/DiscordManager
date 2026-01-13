import discord

from services.buttons.protection.admin_buttons_protection import FirewallButton
from services.other_services.get_channel import ChannelTypeView
from services.factories.channel_factory.scenarios_factory import ChannelScenarioFactory
from services.factories.db_factory.db_scenario_factory import DBScenarioFactory
from services.utils.messages import SYSTEM_MSGS as SM


class SendMessageButton(FirewallButton):
    scope = 'admin'

    def __init__(self, db_factory: DBScenarioFactory):
        super().__init__(
            label='Send message',
            style=discord.ButtonStyle.blurple
        )
        self.db_factory = db_factory

    async def on_click(self, interaction: discord.Interaction):
        self.view.disable_all_items()
        scenario = ChannelScenarioFactory.for_db_message_save(self.db_factory)

        view = ChannelTypeView(
            scenario,
            text_only=True
        )

        try:
            await interaction.user.send(SM.get('ask_private_channel_msg'), view=view)

            await interaction.edit_original_response(
                content=SM.get('ask_private_msg')
            )
        except discord.Forbidden:
            await interaction.edit_original_response(
                content=SM.get('send_message_failure_msg')
            )
