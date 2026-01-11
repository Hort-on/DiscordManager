import discord

from modules.birthdays.birthday_repo import BirthdayManager

from modules.buttons.general_buttons.buttons_for_admins.birthday_button.birthday_menu_view import BirthdayMenuView


class BirthdayMenuButton(discord.ui.Button):
    def __init__(self, birthday_manager: BirthdayManager):
        super().__init__(
            label='🎂 Birthdays',
            style=discord.ButtonStyle.secondary
        )
        self.birthday_manager = birthday_manager

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            content='🎂 Birthday management',
            view=BirthdayMenuView(interaction.guild_id, self.birthday_manager)
        )
