import discord

from modules.buttons.buttons_for_admins.birthday_button.service.birthday_delete_button_func.BirthdayModal import \
    DeleteBirthdayModal


class DeleteBirthdayButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Delete birthday',
            style=discord.ButtonStyle.red
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.disable_all_items()
        await interaction.response.send_modal(DeleteBirthdayModal())
