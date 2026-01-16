import discord

from services.buttons.protection.admin_buttons_protection import FirewallButton
from services.other_services.get_channel import ChannelSelectorManager
from services.factories.channel_factory.scenarios_factory import ChannelScenarioFactory
from services.factories.db_factory.db_scenario_factory import DBScenarioFactory


class SendMessageButton(FirewallButton):
    scope = 'admin'

    def __init__(self, db_factory: DBScenarioFactory):
        super().__init__(
            label='Send message',
            style=discord.ButtonStyle.blurple
        )
        self.db_factory = db_factory

    async def on_click(self, interaction: discord.Interaction):
        scenario = ChannelScenarioFactory.for_db_message_save(db_factory=self.db_factory)

        manager = ChannelSelectorManager(scenario=scenario, text_only=True)

        try:
            await interaction.user.create_dm()
            await manager.select_channel_type(interaction=interaction)
        except discord.Forbidden:
            await interaction.edit_original_response(
                content=''
            )
