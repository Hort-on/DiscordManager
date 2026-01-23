import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton
from modules.buttons.for_admins.superusers_buttons.modals import AddSuperusersModal
from modules.buttons.for_admins.superusers_buttons.services import DeleteSuperuserService, GetSuperusersList


class AddSuperuserButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Add super user',
            style=discord.ButtonStyle.green
        )

    async def on_click(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(AddSuperusersModal())


class DeleteSuperusersButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Delete superusers',
            style=discord.ButtonStyle.green,
        )
        self.del_superuser = DeleteSuperuserService()

    async def on_click(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await self.del_superuser.prepare_users(interaction=interaction)


class SuperusersListButton(FirewallButton):
    scope = 'admin'

    def __init__(self):
        super().__init__(
            label='Show current superusers',
            style=discord.ButtonStyle.green,
        )
        self.get_superuser_name = GetSuperusersList()

    async def on_click(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        result = self.get_superuser_name.get_display(guild=interaction.guild)
        await interaction.edit_original_response(content=result)
