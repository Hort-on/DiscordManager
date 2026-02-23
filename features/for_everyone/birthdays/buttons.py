import discord

from features.for_everyone.birthdays.modals import AddBirthdayModal, DeleteBirthdayModal


class AddBirthdayButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Add birthday',
            style=discord.ButtonStyle.blurple
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(AddBirthdayModal())


class DeleteBirthdayButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Delete birthday',
            style=discord.ButtonStyle.red
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(DeleteBirthdayModal())
