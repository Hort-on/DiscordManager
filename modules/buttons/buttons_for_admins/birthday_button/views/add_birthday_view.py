import discord

from modules.buttons.buttons_for_admins.birthday_button.service.birthday_add_button_func.BirthdayModal import \
    AddBirthdayModal


class AddBirthdayButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Add birthday",
            style=discord.ButtonStyle.blurple
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        self.view.disable_all_items()
        await interaction.response.send_modal(AddBirthdayModal())
