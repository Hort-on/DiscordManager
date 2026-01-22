import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.management.verification.modals import AgreeModal

from services.embed_constructor.embed_constructor import InfoEmbed


class AgreeButton(FirewallButton):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='Agree',
            style=discord.ButtonStyle.blurple,
            custom_id='verify_agree'
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(AgreeModal())


class DisagreeButton(FirewallButton):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='Disagree',
            style=discord.ButtonStyle.red,
            custom_id='verify_disagree'
        )

    async def on_click(self, interaction: discord.Interaction):
        info_embed = InfoEmbed(
            description='You have declined the rules, you will not be given an access to this server,'
                        ' until you agree with the rules.'
        )
        await interaction.response.send_message(
            embed=info_embed,
            ephemeral=True
        )
