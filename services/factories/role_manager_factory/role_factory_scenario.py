import discord
from discord import ui

from database.settings_storage.settings_storage import SettingsStorage
from database.settings_storage.settings_storage_manager import StorageTarget


class BaseRoleScenario(ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    def role_proceed(self, interaction: discord.Interaction):
        raise NotImplementedError


class AddRoleManagerScenario(BaseRoleScenario):
    def __init__(self, settings: SettingsStorage):
        super().__init__()
        self.settings = settings
        self.roles = []

    async def role_proceed(self, interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            return

        hidden_roles = self.settings.set_storage.get_set(
            StorageTarget.HIDDEN_ROLES,
            interaction.guild_id
        )
        member = guild.get_member(interaction.user.id)
        if not member:
            return

        member_roles = member.roles

        for role in interaction.guild.roles:
            if role.is_default():
                continue

            if role >= guild.me.top_role:
                continue

            if role.id not in hidden_roles and role not in member_roles:
                self.roles.append({
                    "id": role.id,
                    "name": role.name
                })

    ..


class DeleteRoleManagerScenario(BaseRoleScenario):
    def __init__(self):
        super().__init__()
        self.member_roles = []

    async def role_proceed(self, interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            return

        member = guild.get_member(interaction.user.id)
        if not member:
            return

        member_roles = member.roles

        for role in member_roles:
            if role.is_default():
                continue

            if role >= guild.me.top_role:
                continue

            self.member_roles.append({
                "id": role.id,
                "name": role.name
            })

    ...


class ShowOptions(BaseRoleScenario):
