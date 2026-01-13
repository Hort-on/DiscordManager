import discord

from services.buttons.protection.admin_buttons_protection import FirewallButton
from services.modals.random_modal.team_by_msg import RandomTeamByMsgModal


class RandomTeamByMsg(FirewallButton):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='Random number',
            style=discord.ButtonStyle.secondary
        )

    async def on_click(self, interaction: discord.Interaction):
        await interaction.send_modal(RandomTeamByMsgModal())
