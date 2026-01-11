import discord

from modules.buttons.general_buttons.buttons_for_users.random_buttons.random_mode_view import RandomModeView


class RandomStartButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='🎲 Randomizer',
            style=discord.ButtonStyle.blurple
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()

        await interaction.edit_original_response(
            content="Choose randomizer mode:",
            view=RandomModeView()
        )
