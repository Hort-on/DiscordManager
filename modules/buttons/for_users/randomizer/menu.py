import discord

from modules.buttons.for_users.randomizer.menu_view import RandomModeView
from modules.buttons.services.protection.admin_buttons_protection import FirewallButton


class RandomMenuButton(FirewallButton):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='🎲 Randomizer',
            style=discord.ButtonStyle.blurple
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        await interaction.edit_original_response(
            content='Choose randomizer mode:',
            view=RandomModeView().prepare(
                guild_id=interaction.guild_id,
                user_id=interaction.user.id
            )
        )
