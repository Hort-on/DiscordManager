import discord

from modules.buttons.services.protection.admin_buttons_protection import FirewallButton

from services.other_services.get_channel import ChannelSelectorManager
from services.factories.channel_factory.scenarios_factory import ChannelFactory


class SendMessageButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Send message',
            style=discord.ButtonStyle.blurple
        )

    async def on_click(self, interaction: discord.Interaction):
        scenario = ChannelFactory.for_db_message_save()

        manager = ChannelSelectorManager(scenario=scenario, text_only=True)

        try:
            await interaction.user.create_dm()
            await manager.select_channel_type(interaction=interaction)
        except discord.Forbidden:
            await interaction.edit_original_response(
                content=''
            )
