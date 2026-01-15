import discord

from modules.buttons.views.for_users.random_mode import RandomModeView

from services.buttons.protection.admin_buttons_protection import FirewallButton


class RandomMenuButton(FirewallButton):
    scope = 'user'

    def __init__(self):
        super().__init__(
            label='🎲 Randomizer',
            style=discord.ButtonStyle.blurple
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()

        await interaction.edit_original_response(
            content='Choose randomizer mode:',
            view=RandomModeView(
                guild_id=interaction.guild_id,
                user_id=interaction.user.id
            )
        )
