import discord

from database.settings_storage.settings import SettingsStorage


class ButtonProtectionService:
    def __init__(self, settings: SettingsStorage):
        from general_services.other_services.is_superuser import IsSuperuserService
        self.admin_service = IsSuperuserService(settings=settings)

    def has_access(
            self,
            interaction: discord.Interaction,
            scope: str
    ) -> bool:
        if scope == 'user':
            return True

        if scope == 'admin':
            return self.admin_service.is_superuser(
                guild=interaction.guild,
                user_id=interaction.user.id
            )

        return False
